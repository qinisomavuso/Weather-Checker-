import os
from dotenv import load_dotenv
from weather_app import WeatherApp
from cli_interface import main as cli_main
from gui_interface import WeatherGUI

load_dotenv()
API_KEY = "a53c475e1da99d22eb6c4e13fef92a50"

if not API_KEY:
    print("Please set OPENWEATHER_API_KEY in .env file")
    exit()

# -----------------------------
# OpenWeatherMap API Settings
# -----------------------------
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# -----------------------------
# Function to fetch weather
# -----------------------------
def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }
    try:
        import requests
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error {response.status_code}: {response.json().get('message')}")
            return None
    except Exception as e:
        print("Error fetching data:", e)
        return None

# -----------------------------
# Function to display relevant info
# -----------------------------
def display_weather(data):
    if not data:
        print("No weather data available.")
        return

    city = data.get("name")
    country = data.get("sys", {}).get("country")
    temp = data.get("main", {}).get("temp")
    feels_like = data.get("main", {}).get("feels_like")
    humidity = data.get("main", {}).get("humidity")
    wind_speed = data.get("wind", {}).get("speed")
    description = data.get("weather")[0]["description"]

    print(f"Weather in {city}, {country}:")
    print(f"  Condition: {description}")
    print(f"  Temperature: {temp}°C (feels like {feels_like}°C)")
    print(f"  Humidity: {humidity}%")
    print(f"  Wind Speed: {wind_speed} m/s")

# -----------------------------
# Run the code
# -----------------------------
if __name__ == "__main__":
    print("Weather App")
    print("1. CLI Interface")
    print("2. GUI Interface")
    print("3. Simple Test (Cape Town)")
    
    choice = input("Choose an option: ")
    
    if choice == '1':
        cli_main(API_KEY)
    elif choice == '2':
        app = WeatherApp(API_KEY)
        gui = WeatherGUI(app)
        gui.run()
    elif choice == '3':
        city_name = "Cape Town"  # Change to any city
        weather_data = get_weather(city_name)
        display_weather(weather_data)
    else:
        print("Invalid choice")

def get_forecast(self, city):
    url = f"{self.base_url}/forecast"
    params = {'q': city, 'appid': self.api_key, 'units': 'metric'}
    response = requests.get(url, params=params)
    return response.json()