from __future__ import print_function, unicode_literals

import utils.logging as logging
from googleapiclient.discovery import build
import pafy
import os
import vlc
os.add_dll_directory(os.getcwd())
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

YOUTUBE_API_KEY = 'AIzaSyAWL17pz25HzMsotaiUtDCAzcbwB03mo5A'

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def search(query):
    request = youtube.search().list(
        part='id,snippet',
        q=query,
        maxResults=5,
        type='video'
    )

    response = request.execute()

    search_results = []

    for video in response['items']:
        title = video["snippet"]["title"]
        video_id = video["id"]["videoId"]
        item = {
            'name': title,
            'value': f'https://www.youtube.com/watch?v={video_id}',
        }

        search_results.append(item)

    return search_results

#########




def play_song(url):
    is_opening = False
    is_playing = False

    video = pafy.new(url)
    best = video.getbestaudio()
    play_url = best.url

    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(play_url)
    media.get_mrl()
    player.set_media(media)
    player.play()

    good_states = [
        "State.Playing",
        "State.NothingSpecial",
        "State.Opening"
    ]

    while str(player.get_state()) in good_states:
        if str(player.get_state()) == "State.Opening" and is_opening is False:
            logging.info("Status: Loading")
            is_opening = True

        if str(player.get_state()) == "State.Playing" and is_playing is False:
            logging.info("Status: Playing")
            is_playing = True

    logging.info("Status: Finish")
    player.stop()

########"""

EXIT_TOGGLE = False


def main(name):
    questions = [
        {
            'type': 'input',
            'name': 'query',
            'message': 'Search:',
        }
    ]

    query = {'query':str(name)}
    logging.info(str(query))
    search_results = search(query.get("query"))
    choice = list_search_results(search_results)
    logging.info(str(choice))
    play_song(choice['search'])
    exit()


def list_search_results(search_list):
    questions = [
        {
            'type': 'list',
            'name': 'search',
            'message': 'Search Results:',
            'choices': search_list,
        },
    ]

    #answer = prompt(questions)
    logging.debug(str(search_list[0]))
    search_list = search_list[0]
    del search_list['name']
    answer = search_list
    answer['search'] = answer['value']
    del answer['value']
    logging.debug(str(answer))
    return answer


