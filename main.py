from weather.weather_flow import WeatherFlow



def mainloop(wf):
    try:
        while True:
            try:
                city = input("City >> ")
                weather = wf.get_weather(city)
                
                #TODO move line 14-40 into a separate WeatherFlow.parse_weather() method, adjust loop logic so the if statement (19-30) makes the method return
                # false and break the loop that way otherwise have the method return all the variables on lines 31-33. Not sure how I'll handle the exceptions yet.
                location = weather.get("location", {})
                current =  weather.get("current", {})
                condition = current.get("condition", {})

                if location is None or current is None or condition is None:
                    print("Error: Missing essential weather data, program will not function as intended without it.")
                    try_again = input("Would you like to try another city? y/n: ")
                    
                    if try_again.lower() == "y":
                        continue
                    elif try_again.lower == "n":
                        print("Exiting...")
                        break
                    else:
                        print("Another key was pressed, exiting...")
                        break

                name, region = location.get("name", "Unknown"), location.get("region", "Unknown")
                temp_c, temp_f = current.get("temp_c", "Unknown temp"), current.get("temp_f", "Unknown temp" )
                text = condition.get("text", "Unknown condition")
                
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