import requests
from datetime import datetime
from typing import Any

class WeatherFlow:

    def __init__(self):
        pass

    def get_weather(self, location: str) -> dict[str, Any] | None:
        """
        Makes a request to aws EC2 server to make the api call and return a json/dictionary of the weather data in the given location.

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
        """
        EC2_URL = 'http://ec2-3-129-211-177.us-east-2.compute.amazonaws.com:8000/weather'

        try:
            payload = {
                'location' : location
            }

            response = requests.post(EC2_URL, json=payload)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f'Request error occured: {e}')
            return None

    def parse_weather(self, weather: dict) -> tuple[str, str, str, str, str, str, str, str, str, str, str]:
        """
        Parses weather dictionary from API and returns extracted data.
        Params: Expects json that is returned from API call made in get_weather.
        """
        # Checking if api actually returned data
        if weather is None:
            raise ValueError('Check that location is valid and try again')
        else:
            location = weather.get('location', {})
            current =  weather.get('current', {})
            condition = current.get('condition', {})

            # Retreiving items from dictionary returned from API and returning them as a tuple
            name, region = location.get('name', 'Unknown'), location.get('region', 'Unknown')
            country = location.get('country', 'Unknown')
            text = condition.get('text', 'Unknown condition') 
            icon = condition.get('icon', 'Icon unavailable')
            
            # Imperial data
            temp_f = current.get('temp_f', 'Unknown temp' )
            feelslike_f = current.get('feelslike_f', 'Unknown')
            wind_mph = current.get('wind_mph', 'Wind speed unknown')

            # Metric data
            temp_c = current.get('temp_c', 'Unknown temp')
            feelslike_c =  current.get('feelslike_c', 'Unknown')
            wind_kph = current.get('wind_kph', 'Wind speed unknown')

            return name, region, country, text, icon, temp_f, feelslike_f, wind_mph, temp_c, feelslike_c, wind_kph
        
    def verbose_weather(self, weather: dict) -> tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str]:
        """
        Grabs the extra values from the API response that will be included in verbose output.
        Params: Expects json object that is returned from API call in get_weather.
        """
        if weather is None:
            raise ValueError('Check that location is valid and try again')
        current = weather.get('current', {})
        air_quality = current.get('air_quality', {})

        
        humidity = current.get('humidity', 'Humidity unavailable')
        uv = current.get('uv', 'UV index unavailable')
        aqi = air_quality.get('us-epa-index', 'Air quality index unavaialble')

        # Imperial values
        precip_in = current.get('precip_in', 'Precipitation unavailable')
        dewpoint_f = current.get('dewpoint_f', 'Dewpoint unavailable')
        vis_miles = current.get('vis_miles', 'Visibility unavailable')
        windchill_f = current.get('windchill_f', 'Windchill unavailable')
        heatindex_f = current.get('heatindex_f', 'Heat index unavailable')
        gust_mph = current.get('gust_mph', 'Wind gust unavailable')

        # Metric values
        precip_mm = current.get('precip_mm', 'Precipitation unavailable')
        dewpoint_c = current.get('dewpoint_c', 'Dewpoint unavailable')
        vis_km = current.get('vis_km', 'Visibility unavailable')
        windchill_c = current.get('windchill_c', 'Windchill unavailable')
        heatindex_c = current.get('heatindex_c', 'Heat index unavailable')
        gust_kph = current.get('gust_kph', 'Wind gust unavailable')
        
        return humidity, uv, aqi, precip_in, dewpoint_f, vis_miles, windchill_f, heatindex_f, gust_mph, precip_mm, dewpoint_c, vis_km, windchill_c, heatindex_c, gust_kph
        

    
    def parse_forecast(self, forcast: dict, metric: bool = False) -> None:
        """
        Parses forcast for the week from the API call, loops through values and prints to console.
        Params: Expects json object that is returned from API call in get_weather.
        """
        forcast_days = forcast.get('forecast', {}).get('forecastday', [])

        # Loop through the list value linked to the key, 'forecastday' in the api response and store needed values
        for day in forcast_days:
            date = day.get('date', 'Date unavailable')
            day_of_week = WeatherFlow._get_day_of_week(date)
            condition = day.get('day', {}).get('condition', {}).get('text', 'Condition not available')
            if not metric:
                maxtemp_f, mintemp_f = day.get('day', {}).get('maxtemp_f'), day.get('day', {}).get('mintemp_f')
                avgtemp_f = day.get('day', {}).get('avgtemp_f')

                print(f'Forecast for {day_of_week}, {date} >> {condition}: {maxtemp_f}\u00b0F/{mintemp_f}\u00b0F Avg: {avgtemp_f}\u00b0F \n')
            else:
                maxtemp_c, mintemp_c = day.get('day', {}).get('maxtemp_c'), day.get('day', {}).get('mintemp_c')
                avgtemp_c = day.get('day', {}).get('avgtemp_c')

                print(f'Forecast for {day_of_week}, {date} >> {condition}: {maxtemp_c}\u00b0C/{mintemp_c}\u00b0C Avg : {avgtemp_c}\u00b0C \n')

    @staticmethod
    def _get_day_of_week(date: str) -> str:
        """
        Helper method that returns day of the week from a day given in YYYY-MM-DD format
        """
        return datetime.strptime(date, '%Y-%m-%d').strftime('%A')
