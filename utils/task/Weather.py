import requests
import datetime
api_key='8ef61edcf1c576d65d836254e11ea420'

import utils.logging as logging
import utils.nlp.parse as parse
import math

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def parse_datetime_object(day: str):
    try: 
        if '.' in day: day = day.split('.')[0]   # %Y-%m-%d %H:%M:%S.%f
        return datetime.datetime.strptime(day, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logging.fail(e) 
        raise ValueError(f"time data '{day}' does not match format '%Y-%m-%d %H:%M:%S'.")




def main(place='here', day='today'):
    place = parse.place_city(place)
    day = str(parse.Time(str(day)))
    parsed_date = parse_datetime_object(day)
    parsed_date = parsed_date.strftime("%Y-%m-%d")
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={api_key}'
    response = requests.get(forecast_url)

    if response.status_code == 200:
        data = response.json()
        forecasts = data['list']  # This contains the forecast data for multiple timestamps
        
        # Create a dictionary to group forecasts by date
        grouped_forecasts = {}
        
        for forecast in forecasts:
            timestamp = forecast['dt']
            date = datetime.datetime.utcfromtimestamp(timestamp).date()  # Get the date from the timestamp
            
            if date not in grouped_forecasts:
                grouped_forecasts[date] = forecast
        
        for date, forecast in grouped_forecasts.items():
            if str(date) == str(parsed_date):
                #timestamp = forecast['dt']
                temp = forecast['main']['temp']
                desc = forecast['weather'][0]['description']
                
                #_date = date.strftime("%d of %B of %Y")
                #_date = _date.replace(_date[_date.find("of")+3], months[date.month - 1])

                #return f'in {_date}, on timestamp {timestamp}, the temperature will be arround {temp} Kelvin or {math.ceil(temp- 273.15)} degrees Celcius, and the description is {desc}.'
                #return f'the temperature will be arround {temp} Kelvin or {math.ceil(temp- 273.15)} degrees Celcius, and the description is {desc}.'
                return  f'{desc} with an expected high of {math.ceil(temp- 273.15)} degrees Celcius.'
        logging.fail('weather forecasts can only be fetched for up to 5 days in advance!\nIf you are seing this message it means that you requested an "out of bounds" date or that your date was not parsed correctly')
        return f'Unfortunatly I can only provide weather forecasts for up to five days in advance from the current date. Is there anything else I can assist you with?'

if __name__ == "__main__":
    print(main())