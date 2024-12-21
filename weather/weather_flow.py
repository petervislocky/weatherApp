import requests
from weather.config import API_KEY

class WeatherFlow:
    
    def __init__(self):
        pass

    def get_weather(self, location):
        """
        Uses the api key to return a dictionary of the weather data in the given location
        """
        if not location:
            raise ValueError("City name cannot be empty")
            
        current_weather_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
        forecast_weather_url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=7&aqi=no&alerts=no"
        current_weather_response = requests.get(current_weather_url)
        forecast_weather_response = requests.get(forecast_weather_url)

        # Raise an error if responses are not successful
        current_weather_response.raise_for_status()
        forecast_weather_response.raise_for_status()

        return current_weather_response.json(), forecast_weather_response.json()

    def parse_weather(self, weather):
        """
        Parses weather dictionary from API and returns extracted data
        """
        location = weather.get("location", {})
        current =  weather.get("current", {})
        condition = current.get("condition", {})

        # Checks if location data is missing and prompts user to try again if yes. Possibly remove this logic
        if location is None or current is None or condition is None:
            print("Error: Missing essential weather data, program will not function as intended without it.")
            try_again = input("Would you like to try another location? y/n: ")
                    
            if try_again.lower() == "y":
                return True
            elif try_again.lower == "n":
                print("Exiting...")
                return False
            else:
                print("Another key was pressed, exiting...")
                return False

        # Retreiving items from dictionary returned from API and returning them as a tuple
        name, region = location.get("name", "Unknown"), location.get("region", "Unknown")
        temp_c, temp_f = current.get("temp_c", "Unknown temp"), current.get("temp_f", "Unknown temp" )
        text = condition.get("text", "Unknown condition") 
        icon = condition.get("icon", "Icon unavailable")
        feelslike_c, feelslike_f = current.get("feelslike_c", "Unknown"), current.get("feelslike_f", "Unknown")
        wind_mph = current.get("wind_mph", "Wind speed unknown")

        return name, region, temp_c, temp_f, text, icon, feelslike_c, feelslike_f, wind_mph
    
    def parse_forcast(self, forcast):
        """TODO
        create new method for parsing forcast data to avoid cluttering up parse_weather()"""
        pass