import requests

from weather.weather_flow import WeatherFlow
from weather.ASCIIicons import ascii_icon

#TODO use google geolocating API to get user location
#TODO create a new method to parse forcast weather
#TODO include input sanitization to clean up user input to prevent malformed or unexpected input
#TODO Try to get the ascii_magic art to print next to the text output instead of underneath it

def mainloop(wf) -> None:
    try:
        while True:
            try:
                location = input("City, State >> ")

                # Feeding location to the API via get_weather method
                weather = wf.get_weather(location)
                # Parsing current weather data returned by API
                current_parsed = wf.parse_weather(weather)
              
                # Assigned values returned from parse_weather and parse_forecast
                name, region, temp_c, temp_f, text, icon, feelslike_c, feelslike_f, wind_mph = current_parsed

                # For debugging
                # print("Full JSON response: ", weather)
                
                print(f"Showing weather for {name}, {region}\n"
                      f"Temp >> {temp_f}\u00b0F / {temp_c}\u00b0C\n"
                      f"Feels like >> {feelslike_f}\u00b0F / {feelslike_c}\u00b0C\n"
                      f"Wind >> {wind_mph}mph\n"
                      f"Conditions >> {text} ")
                ascii_icon(icon)
                # Call parse_weather to loop through forecast values and print to console
                print("Next week forecast\n")
                wf.parse_forecast(weather)
                break

            except ValueError as e:
                print(f"Data error: {e}")
            except requests.exceptions.RequestException as e:
                print(f"HTTP/HTTPS request error: {e}\nCommon causes for this error are,\n"
                      "Inputting a location that does not exist\n"
                      "No internet connection\n"
                      "Server-side errors")
            except Exception as e:
                print(f"Unexpected error occured: {e}")
            
    except KeyboardInterrupt as k:
        print("\nKeyboard interrupt detected, exiting program ")

def main():
    wf = WeatherFlow()
    mainloop(wf)

if __name__ == "__main__":
    main()