from geotext import GeoText
import urllib.request
import json

import utils.nlp.parse as parse
from datetime import datetime
import pytz

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def get_timezone(city_name):
    geolocator = Nominatim(user_agent="timezone_app")
    location = geolocator.geocode(city_name)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
        
        timezone_finder = TimezoneFinder()
        timezone_str = timezone_finder.timezone_at(lng=longitude, lat=latitude)
        return timezone_str
    else:
        raise ValueError('Unable to parse city Name!')

def main(place=None):  
    if place == None: timezone = None 
    else:
        try:
            location = get_timezone(parse.place_city(place))
            timezone = pytz.timezone(location)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f'Unable to fetch time for timezone of {location}.')
        except Exception as e:
            raise ValueError(f'Error while fetching time "{e}".')
        
    current_time = datetime.now(timezone)
    
    # Format the time as "hh:mm TT" (with AM/PM), replacing 12:00 and 00:00
    formatted_time = current_time.strftime("%I:%M %p, %Z")
    
    # Replace 12:00 with "midday and", and 00:00 with "midnight and"
    if formatted_time.startswith("12:"):
        formatted_time = formatted_time.replace("12:", "midday and ", 1)
    elif formatted_time.startswith("00:"):
        formatted_time = formatted_time.replace("00:", "midnight and ", 1)
    
    return formatted_time#, location

#print(main('Braga'))