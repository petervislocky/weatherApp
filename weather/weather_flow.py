import requests

from weather.config import API_KEY

class WeatherFlow:
    
    def __init__(self):
        pass

    def get_weather(self, location) -> str:
        """
        Uses the api key to return a dictionary of the weather data in the given location
        """
        if not location:
            raise ValueError("City name cannot be empty")

        weather_url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=7&aqi=no&alerts=no"
        weather_response = requests.get(weather_url)

        # Raise an error if responses are not successful
        weather_response.raise_for_status()

        return weather_response.json()

    def parse_weather(self, weather) -> str:
        """
        Parses weather dictionary from API and returns extracted data
        """
        location = weather.get("location", {})
        current =  weather.get("current", {})
        condition = current.get("condition", {})

        # Checks if location data is missing
        if location is None or current is None or condition is None:
            raise ValueError("Weather data from API was not returned, and cannot be parsed, as expected")

        # Retreiving items from dictionary returned from API and returning them as a tuple
        name, region = location.get("name", "Unknown"), location.get("region", "Unknown")
        temp_c, temp_f = current.get("temp_c", "Unknown temp"), current.get("temp_f", "Unknown temp" )
        text = condition.get("text", "Unknown condition") 
        icon = condition.get("icon", "Icon unavailable")
        feelslike_c, feelslike_f = current.get("feelslike_c", "Unknown"), current.get("feelslike_f", "Unknown")
        wind_mph = current.get("wind_mph", "Wind speed unknown")

        return name, region, temp_c, temp_f, text, icon, feelslike_c, feelslike_f, wind_mph
    
    def parse_forecast(self, forcast) -> None:
        """
        Parses forcast for the week from the API call, loops through values and prints to console
        """
        forcast_days = forcast.get("forecast", {}).get("forecastday", [])

        # Loop through the list value linked to the key, "forecastday" in the api json dictionary response and store needed values
        for day in forcast_days:
            date = day.get("date", "Date unavailable")
            condition = day.get("day", {}).get("condition", {}).get("text", "Condition not available")
            maxtemp_f = day.get("day", {}).get("maxtemp_f")
            mintemp_f = day.get("day", {}).get("mintemp_f")
            avgtemp_f = day.get("day", {}).get("avgtemp_f")

            print(f"Forecast for {date} >> {condition}: {maxtemp_f}\u00b0F/{mintemp_f}\u00b0F Avg: {avgtemp_f}\u00b0F \n")