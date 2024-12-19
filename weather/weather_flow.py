import requests
from weather.config import API_KEY

class WeatherFlow:
    
    def __init__(self):
        pass

    def get_weather(self, city):
        """
        Uses the api key to return a dictionary of the weather data in the given city
        """
        if not city:
            raise ValueError("City name cannot be empty")
            
        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        response = requests.get(url)

        # Raise an error if the response is not successful
        response.raise_for_status()\
            
        return response.json()

    def parse_weather(self, weather):
        """
        Parses weather dictionary from API and returns extracted data
        """
        location = weather.get("location", {})
        current =  weather.get("current", {})
        condition = current.get("condition", {})

        if location is None or current is None or condition is None:
            print("Error: Missing essential weather data, program will not function as intended without it.")
            try_again = input("Would you like to try another city? y/n: ")
                    
            if try_again.lower() == "y":
                return True
            elif try_again.lower == "n":
                print("Exiting...")
                return False
            else:
                print("Another key was pressed, exiting...")
                return False

        name, region = location.get("name", "Unknown"), location.get("region", "Unknown")
        temp_c, temp_f = current.get("temp_c", "Unknown temp"), current.get("temp_f", "Unknown temp" )
        text, icon = condition.get("text", "Unknown condition"), condition.get("icon", "Icon unavailable")
        
        return name, region, temp_c, temp_f, text, icon
    