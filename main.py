import requests
import argparse
import sys

from weather.weather_flow import WeatherFlow
from weather.ASCIIicons import ascii_icon

'''
Docs are pretty extensive because I want to be able to understand what I was doing when I come back to this code in the future, and also to help others understand what I was doing
Author: @PeterVislocky
'''
#TODO update error handling to be more specific, particularly for catching NoneType errors that occur when the location does not exist so the api returns None
#TODO add a bunch of other options for things like verbose output, sunset times, alerts (which would involve editing the backend script to 
# accept that as a parameter), etc

def mainloop(wf: WeatherFlow, location: str = None, metric: bool = False) -> None:
    '''
    Main program logic
    Params: WeatherFlow object instance
    '''
    try:
        try:
            if location is None:    
                location = input('Enter a location >> ')

            weather = wf.get_weather(location)    # Feeding location to the API via get_weather method
            current_parsed = wf.parse_weather(weather)    # Parsing current weather data returned by API
            
            # Assigned values returned from parse_weather and parse_forecast
            name, region, country, text, icon, temp_f, feelslike_f, wind_mph, temp_c, feelslike_c, wind_kph = current_parsed
            
            # print('Full JSON response: ', weather)    # For debugging
            
            # Formatting values to be displayed in the console
            country_format = f', {country}' if country != 'United States of America' else ''
            temp_format = f'{temp_f}\u00b0F' if not metric else f'{temp_c}\u00b0C'
            feelslike_format = f'{feelslike_f}\u00b0F' if not metric else f'{feelslike_c}\u00b0C'
            wind_format = f'{wind_mph} mph' if not metric else f'{wind_kph} kph'

            print(f'Showing weather for {name}, {region}{country_format}\n'
                    f'Temp >> {temp_format}\n'
                    f'Feels like >> {feelslike_format}\n'
                    f'Wind >> {wind_format}\n'
                    f'Conditions >> {text}')
            ascii_icon(icon)
            
            # Call parse_weather to loop through forecast values and print to console
            print('3 day forecast\n')
            wf.parse_forecast(weather, metric)

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
    parser.add_argument(
        '-m', '--metric',
        action='store_true',
        help='Displays units in metric (default is imperial)'
    )
    parser.add_argument(
        '-i', '--imperial',
        action='store_true',
        help='Displays units in imperial (this is the default behavior)'
    )
    args = parser.parse_args()

    # Ensure user doesn't set metric and imperial flags at the same time
    if args.metric and args.imperial:
        print('Error: You cannot set both --metric and --imperial flags at the same time')
        sys.exit(1)

    # If imperial flag is set just set metric to false instead of args.metric, which would be true if the metric flag is set
    metric = args.metric
    if args.imperial:
        metric = False

    wf = WeatherFlow()
    mainloop(wf, args.location, metric)

if __name__ == '__main__':
    main()