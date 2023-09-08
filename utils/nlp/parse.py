from geotext import GeoText
import urllib.request
import json

import dateparser
import datetime
#from datetime import datetime
from timefhuman import timefhuman

def Time(text):
    replacements = {
    'midday': '12 pm',
    'mid day': '12 pm',
    'half day': '12 pm',
    'mid night': 'midnight',
    'half night': 'midnight'
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    text = text.split('from')[0] # it just breaks with smt like 'one minute from now'
    now = datetime.datetime.now()
    try: result = dateparser.parse(text)
    except: result = None
    if result == None:
        return timefhuman(text, now=now)
    return result

def place_city(city_name: str):
    city_name = city_name.split()
    for city_word in city_name:
        try:
            city_word = city_word.capitalize()
            city_word = str(city_word)
            places = GeoText(city_word)
            places = places.cities
            if str(places) != "[]":
                #logging.debug(f"location, {places}", "location")
                break
        except: pass
    try: places = places[0]
    except:
        try:
            from urllib.request import urlopen
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)
            places = data['city']
            #logging.debug(f"(local)location, {places}", "location")
            return places
        except urllib.error.URLError as Connection_Error:
            raise ValueError('Unable to fetch time, no internet connection available!')
    return places