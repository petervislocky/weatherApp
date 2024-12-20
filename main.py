from weather.weather_flow import WeatherFlow
from weather.ASCIIicons import ascii_icon

#TODO use google geolocating API to get user location
#TODO create a new method to parse forcast_weather

def mainloop(wf):
    try:
        while True:
            try:
                location = input("City, State >> ")
                """
                forecast_weather holds the dictionary with the weather forcast values, its not being used yet, but its been implemented so
                all that needs to be done is to create a separate method for parsing forcast data because the dictionary values
                """
                current_weather, forecast_weather = wf.get_weather(location)
                parsed = wf.parse_weather(current_weather)

                if parsed is True:
                    continue
                elif parsed is False:
                    break
                
                name, region, temp_c, temp_f, text, icon, feelslike_c, feelslike_f, wind_mph = parsed

                # For debugging
                # print("Full JSON response: ", current_weather)
                # print("Forcast", forecast_weather)
                
                print(f"Showing weather for {name}, {region}")
                print(f"Temp >> {temp_f}\u00b0F / {temp_c}\u00b0C")
                print(f"Feels like >> {feelslike_f}\u00b0F / {feelslike_c}\u00b0C")
                print(f"Wind >> {wind_mph}mph")
                print(f"Conditions >> {text} ")
                ascii_icon(icon)
                break

            except Exception as e:
                print("Invalid entry try again ")
                continue
            
    except KeyboardInterrupt as k:
        print("\nKeyboard interrupt detected, exiting program ")

def main():
    wf = WeatherFlow()
    mainloop(wf)

if __name__ == "__main__":
    main()