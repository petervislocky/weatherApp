import requests

from weather.weather_flow import WeatherFlow
from weather.ASCIIicons import ascii_icon

#TODO use google geolocating API to get user location
#TODO include input sanitization to clean up user input to prevent malformed or unexpected input

def mainloop(wf: WeatherFlow) -> None:
    '''
    Main program logic
    Params: WeatherFlow object instance
    '''
    try:
        while True:
            try:
                location = input('City, State/Country >> ')

                weather = wf.get_weather(location)    # Feeding location to the API via get_weather method
                current_parsed = wf.parse_weather(weather)    # Parsing current weather data returned by API
              
                # Assigned values returned from parse_weather and parse_forecast
                name, region, temp_c, temp_f, text, icon, feelslike_c, feelslike_f, wind_mph = current_parsed
                
                # print('Full JSON response: ', weather)    # For debugging
                
                ascii_art_lines = ascii_icon(icon)    # Generate ascii art and store in var

                # Prepare weather text lines so they can be displayed next to ascii art instead of above it, each line starts with the unicode reset character to remove any color formatting the ascii art library left behind
                weather_text_lines = [
                    f'\033[0m Showing weather for {name}, {region}',
                      f'\033[0m Temp >> {temp_f}\u00b0F / {temp_c}\u00b0C',
                      f'\033[0m Feels like >> {feelslike_f}\u00b0F / {feelslike_c}\u00b0C',
                      f'\033[0m Wind >> {wind_mph}mph',
                      f'\033[0m Conditions >> {text} '
                ]

                # Join ascii art and the text to be printed into one string
                print('\n'.join(
                    f'{ascii_line:<50} {weather_line}'
                    for ascii_line, weather_line in zip(ascii_art_lines, weather_text_lines)
                ))

                # Prints remaining lines of ASCII art
                remaining_ascii = ascii_art_lines[len(weather_text_lines):]
                for line in remaining_ascii:
                    print(line)
               
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
    wf = WeatherFlow()
    mainloop(wf)

if __name__ == '__main__':
    main()