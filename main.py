import requests
import argparse
import sys

from weather.weather_flow import WeatherFlow
from weather.ASCIIicons import ascii_icon

'''
CLI based weather app that shows weather, plus forecast for given area, supports metric and imperial units
Author: @PeterVislocky
'''

def mainloop(wf: WeatherFlow, location: str = None, metric: bool = False, verbose: bool = False) -> None:
    '''
    Main program logic
    Params: WeatherFlow object instance
    '''
    try:
        try:
            if location is None:    
                location = input('Enter a location >> ')

            weather = wf.get_weather(location)
            current_parsed = wf.parse_weather(weather)
            
            name, region, country, text, icon, temp_f, feelslike_f, wind_mph, temp_c, feelslike_c, wind_kph = current_parsed
            
            # print('Full JSON response: ', weather)    # For debugging
            
            # Standard output
            # Formatting values to be displayed in the console
            region_format = f'{region}, ' if region != '' else ''
            country_format = f'{country}' if country != 'United States of America' else ''
            temp_format = f'{temp_f}\u00b0F' if not metric else f'{temp_c}\u00b0C'
            feelslike_format = f'{feelslike_f}\u00b0F' if not metric else f'{feelslike_c}\u00b0C'
            wind_format = f'{wind_mph} mph' if not metric else f'{wind_kph} kph'

            print(f'Showing weather for {name}, {region_format}{country_format}\n'
                    f'Temp >> {temp_format}\n'
                    f'Feels like >> {feelslike_format}\n'
                    f'Wind >> {wind_format}\n'
                    f'Conditions >> {text}')
            # Verbose output
            if verbose:
                humidity, uv, aqi, precip_in, dewpoint_f, vis_miles, windchill_f, heatindex_f, gust_mph, precip_mm, dewpoint_c, vis_km, windchill_c, heatindex_c, gust_kph = wf.verbose_weather(weather)
                
                # Format values for metric or imperial
                precip_format = f'{precip_in}in' if not metric else f'{precip_mm}mm'
                dewpoint_format = f'{dewpoint_f}\u00b0F' if not metric else f'{dewpoint_c}\u00b0C'
                vis_format = f'{vis_miles} miles' if not metric else f'{vis_km} km'
                windchill_format = f'{windchill_f}\u00b0F' if not metric else f'{windchill_c}\u00b0C'
                heatindex_format = f'{heatindex_f}\u00b0F' if not metric else f'{heatindex_c}\u00b0C'
                gust_format = f'{gust_mph} mph' if not metric else f'{gust_kph} kph'

                print(f'Gust >> {gust_format}\n'
                      f'Windchill >> {windchill_format}\n'
                      f'Heat Index >> {heatindex_format}\n'
                      f'Humidity >> {humidity}%\n'
                      f'UV Index >> {uv}\n'
                      f'Air Quality Index >> {aqi}\n'
                      f'Precipitation >> {precip_format}\n'
                      f'Dewpoint >> {dewpoint_format}\n'
                      f'Visibility >> {vis_format}\n')
            ascii_icon(icon)
            
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
            
    except KeyboardInterrupt as e:
        print('\nKeyboard interrupt detected, exiting program ')

def main():
    # Parse command line args
    parser = argparse.ArgumentParser(description='CLI based weather app that displays current weather and 3 day forecast for a given location')
    parser.add_argument(
        '-l', '--location',
        type=str,
        metavar='<location>',
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
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Displays verbose output'
    )
    args = parser.parse_args()
 
    if args.metric and args.imperial:
        print('Error: You cannot set both --metric and --imperial flags at the same time')
        sys.exit(1)

    # If imperial flag is set, I'm just setting metric to false instead of args.metric, which would be true if the metric flag is set
    metric = args.metric
    if args.imperial:
        metric = False
    
    wf = WeatherFlow()
    mainloop(wf, args.location, metric, args.verbose)
if __name__ == '__main__':
    main()