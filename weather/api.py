import requests
from weather.config import API_KEY

def get_weather(city):
    """ Uses the api key to return a dictionary of the weather data in the given city"""
    if not city:
        raise ValueError("City name cannot be empty")
        
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)

    #raise an error if the response is not successful
    response.raise_for_status()\
        
    return response.json()


    