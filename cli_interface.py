from weather_app import WeatherApp

def display_weather_cli(weather_data):
    if isinstance(weather_data, dict):
        print("\n" + "="*40)
        print(f"Weather in {weather_data['city']}, {weather_data['country']}")
        print("="*40)
        print(f"Temperature: {weather_data['temperature']}°C")
        print(f"Feels like: {weather_data['feels_like']}°C")
        print(f"Conditions: {weather_data['description']}")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Wind Speed: {weather_data['wind_speed']} m/s")
        print("="*40)
    else:
        print(weather_data)

# Main CLI loop
def main(api_key):
    app = WeatherApp(api_key)
    
    while True:
        print("\n1. Check weather")
        print("2. Add to favorites")
        print("3. View favorites")
        print("4. Exit")
        
        choice = input("\nSelect option: ")
        
        if choice == '1':
            city = input("Enter city: ")
            weather = app.get_current_weather(city)
            display_weather_cli(weather)
        
        elif choice == '2':
            city = input("City to save: ")
            app.save_favorite(city)
            print(f"Saved {city} to favorites!")
        
        elif choice == '3':
            print("\nFavorite Cities:")
            for fav in app.favorites:
                print(f" - {fav}")
        
        elif choice == '4':
            break