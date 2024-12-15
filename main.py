from weather.api import get_weather

def main():
    city = input("City: ")
    weather = get_weather(city)
    print(weather)

if __name__ == "__main__":
    main()