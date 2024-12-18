from weather.weather_flow import WeatherFlow



def mainloop(wf):
    try:
        while True:
            try:
                city = input("City, State >> ")
                weather = wf.get_weather(city)
                parsed = wf.parse_weather(weather)

                if parsed is True:
                    continue
                elif parsed is False:
                    break
                
                name, region, temp_c, temp_f, text = parsed

                #for debugging
                #print("Full JSON response: ", weather)
                
                print(f"Showing weather for {name}, {region}")
                print(f"Temp >> {temp_f}\u00b0F / {temp_c}\u00b0C")
                print(f"Conditions >> {text}")
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