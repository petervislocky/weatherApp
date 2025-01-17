import requests
import argparse

from weather.weather_flow import WeatherFlow
from weather.ASCIIicons import ascii_icon

'''
Docs are pretty extensive because I want to be able to understand what I was doing when I come back to this code in the future, and also to help others understand what I was doing
Author: @PeterVislocky
'''
#TODO add a command line option to specify farhenheit or celsius
#TODO add a bunch of other options for things like verbose output, sunset times, alerts (which would involve editing the backend script to 
# accept that as a parameter), etc

def mainloop(wf: WeatherFlow, location: str = None) -> None:
    '''
    Main program logic
    Params: WeatherFlow object instance
    '''
    try:
        while True:
            try:
                if location is None:    
                    location = input('Enter a location >> ')

                weather = wf.get_weather(location)    # Feeding location to the API via get_weather method
                current_parsed = wf.parse_weather(weather)    # Parsing current weather data returned by API
              
                # Assigned values returned from parse_weather and parse_forecast
                name, region, country, temp_c, temp_f, text, icon, feelslike_c, feelslike_f, wind_mph = current_parsed
                
                # print('Full JSON response: ', weather)    # For debugging
                print( f'Showing weather for {name}, {region}{', ' + country if country != 'United States of America' else ''}\n'
                      f'Temp >> {temp_f}\u00b0F / {temp_c}\u00b0C\n'
                      f'Feels like >> {feelslike_f}\u00b0F / {feelslike_c}\u00b0C\n'
                      f'Wind >> {wind_mph}mph\n'
                      f'Conditions >> {text} ')
                ascii_icon(icon)
               
                # Call parse_weather to loop through forecast values and print to console
                print('3 day forecast\n')
                wf.parse_forecast(weather)
                break

            except ValueError as e:
                print(f'Data error: {e}')
            except requests.exceptions.RequestException as e:
                print(f'HTTP/HTTPS request error: {e}\nCommon causes for this error are,\n'
                      'Inputting a location that does not exist\n'
                      'No internet connection\n'
                      'Server-side errors')
            except Exception as e:
                print(f'Unexpected error occured: {e}')
            
    except KeyboardInterrupt as k:
        print('\nKeyboard interrupt detected, exiting program ')

def main():
    # Parse command line args
    parser = argparse.ArgumentParser(description='CLI based weather app that displays current weather and 3 day forecast for a given location')
    parser.add_argument(
        '-l', '--location',
        type=str,
        help='Specify the location to get the weather for, if not specified, the program will prompt you for a location'
    )
    args = parser.parse_args()

    wf = WeatherFlow()
    mainloop(wf, args.location)

if __name__ == '__main__':
    main()