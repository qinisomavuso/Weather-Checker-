import requests
import json
from datetime import datetime

class WeatherApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.favorites = self.load_favorites()
    
    def get_current_weather(self, city):
        """Fetch current weather for a city"""
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return self._format_weather_data(data)
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather: {e}"
    
    def _format_weather_data(self, data):
        """Extract and format relevant weather information"""
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'].title(),
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon']
        }
    
    def save_favorite(self, city):
        """Save a city to favorites"""
        if city not in self.favorites:
            self.favorites.append(city)
            self._save_favorites()
    
    def load_favorites(self):
        """Load favorites from file"""
        try:
            with open('favorites.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_favorites(self):
        """Save favorites to file"""
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites, f)