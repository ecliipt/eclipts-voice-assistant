from __future__ import print_function, unicode_literals

from googleapiclient.discovery import build
import pafy
import os
import vlc

#import utils.engines.player as player
import utils.logging as logging

import threading

global music_threads
music_threads = []

global music_exit_flag
music_exit_flag = threading.Event()


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
    global music_exit_flag
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
        if music_exit_flag.is_set(): 
            logging.info(f"Music thread '{threading.current_thread().name}' exiting due to exit signal.", wait=False)
            break
            
        if str(player.get_state()) == "State.Opening" and is_opening is False:
            logging.info("Status: Loading")
            is_opening = True

        if str(player.get_state()) == "State.Playing" and is_playing is False:
            logging.info("Status: Playing")
            is_playing = True

    logging.info("Status: Finish")
    player.stop()


def player_fetch(name):
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
    return choice['search']
    #play_song(choice['search'])
    #exit()


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


def kill_threads():
    #alarm_exit_flag = threading.Event()
    music_exit_flag.set()
    for thread in music_threads:
        thread.join()

def main(name=None):
    global music_exit_flag
    music_exit_flag.clear()
    if name == None: raise ValueError('No song name was provided!')
    try:
        name = player_fetch(name)
        music_thread = threading.Thread(target=play_song, args=(name,))
        music_thread.start()
        music_threads.append(music_thread)
        return ''
    except Exception as e: raise ValueError(
        f'Error encountered on music threads: {e}')


"""def playerStream(name):
    global music_exit_flag
    EXIT_FLAG =False
    try: 
        while True:
            if music_exit_flag.is_set(): 
                logging.info(f"Music thread '{threading.current_thread().name}' exiting due to exit signal.", wait=False)
                break
            if EXIT_FLAG: break
            print(1)
            EXIT_FLAG = player.main(name)
    except Exception as e: raise ValueError(
        f'Error encountered on {threading.current_thread().name}: {e}')"""