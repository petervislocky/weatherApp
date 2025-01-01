import requests
import json
from datetime import datetime
from typing import Any

from weather.config import API_KEY

class WeatherFlow:

    def __init__(self):
        pass

    def get_weather(self, location: str) -> dict[str, Any]:
        '''
        Makes a request to aws lambda function to make the api call and return a json/dictionary of the weather data in the given location.
        Days of week are hardcoded as well as alert toggle and aqi toggle.
        
        Return type contains nested dictionaries and lists with str type keys
        Example return value structure:
            {
    "location": {
        "name": "New York",
        "region": "New York",
        "country": "United States of America",
        "lat": 40.7142,
        "lon": -74.0064,
        "tz_id": "America/New_York",
        "localtime_epoch": 1735354653,
        "localtime": "2024-12-27 21:57"
    },
    "current": {
        "last_updated_epoch": 1735353900,
        "last_updated": "2024-12-27 21:45",
        "temp_c": 5.1,
        "temp_f": 41.2,
        "is_day": 0,
        "condition": {
            "text": "Partly cloudy",
            "icon": "//cdn.weatherapi.com/weather/64x64/night/116.png",
            "code": 1003
        }, ...
        '''
        LAMBDA_FUNCTION_URL = 'https://rhou6tbgpwkhrnje5irw5p23wq0kxowe.lambda-url.us-east-2.on.aws/'

        try:
            # Prepare payload
            payload = {
                'location' : location
            }

            print(f'Calling Lambda function with payload: {payload}')   # For debugging
            # Make request to lambda function
            response = requests.post(LAMBDA_FUNCTION_URL, json=payload)

            # Raise an exception if the status code is not 200
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error occured calling Lambda function: {e}')
            return None

    def parse_weather(self, weather: dict) -> tuple[str, str, float, float, str, str, float, float, float]:
        '''
        Parses weather dictionary from API and returns extracted data.
        Params: Expects json that is returned from API call made in get_weather.
        '''
        location = weather.get('location', {})
        current =  weather.get('current', {})
        condition = current.get('condition', {})

        # Checks if location data is missing
        if location is None or current is None or condition is None:
            raise ValueError('Weather data from API was not returned, and cannot be parsed, as expected')

        # Retreiving items from dictionary returned from API and returning them as a tuple
        name, region = location.get('name', 'Unknown'), location.get('region', 'Unknown')
        country = location.get('country', 'Unknown')
        temp_c, temp_f = current.get('temp_c', 'Unknown temp'), current.get('temp_f', 'Unknown temp' )
        text = condition.get('text', 'Unknown condition') 
        icon = condition.get('icon', 'Icon unavailable')
        feelslike_c, feelslike_f = current.get('feelslike_c', 'Unknown'), current.get('feelslike_f', 'Unknown')
        wind_mph = current.get('wind_mph', 'Wind speed unknown')

        return name, region, country, temp_c, temp_f, text, icon, feelslike_c, feelslike_f, wind_mph
    
    def parse_forecast(self, forcast: dict) -> None:
        '''
        Parses forcast for the week from the API call, loops through values and prints to console.
        Params: Expects json object that is returned from API call in get_weather.
        '''
        forcast_days = forcast.get('forecast', {}).get('forecastday', [])

        # Loop through the list value linked to the key, 'forecastday' in the api response and store needed values
        for day in forcast_days:
            date = day.get('date', 'Date unavailable')
            day_of_week = WeatherFlow._get_day_of_week(date)    # Getting day of week from date
            condition = day.get('day', {}).get('condition', {}).get('text', 'Condition not available')
            maxtemp_f, mintemp_f = day.get('day', {}).get('maxtemp_f'), day.get('day', {}).get('mintemp_f')
            avgtemp_f = day.get('day', {}).get('avgtemp_f')

            print(f'Forecast for {day_of_week}, {date} >> {condition}: {maxtemp_f}\u00b0F/{mintemp_f}\u00b0F Avg: {avgtemp_f}\u00b0F \n')

    @staticmethod
    def _get_day_of_week(date: str) -> str:
        '''
        Helper method that returns day of the week from a day given in YYYY-MM-DD fromat
        '''
        return datetime.strptime(date, '%Y-%m-%d').strftime('%A')
