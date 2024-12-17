from weather.weather_flow import WeatherFlow


def main():
    wf = WeatherFlow()
    try:
        while True:
            try:
                city = input("City: ")
                weather = wf.get_weather(city)
                print(weather)
                break
            except Exception as e:
                print("Invalid entry try again ")
                continue
    except KeyboardInterrupt as k:
        print("\nKeyboard interrupt detected, exiting program ")

if __name__ == "__main__":
    main()