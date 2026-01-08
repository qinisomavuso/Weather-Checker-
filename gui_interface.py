import tkinter as tk
from tkinter import ttk, messagebox

class WeatherGUI:
    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.setup_ui()
    
    def setup_ui(self):
        # City entry
        ttk.Label(self.root, text="City:").pack(pady=5)
        self.city_entry = ttk.Entry(self.root, width=30)
        self.city_entry.pack(pady=5)
        
        # Search button
        ttk.Button(self.root, text="Get Weather", 
                  command=self.get_weather).pack(pady=10)
        
        # Weather display frame
        self.weather_frame = ttk.Frame(self.root)
        self.weather_frame.pack(pady=20)
        
        # Favorites list
        self.update_favorites_list()
    
    def get_weather(self):
        city = self.city_entry.get()
        if city:
            weather = self.app.get_current_weather(city)
            self.display_weather(weather)
    
    def display_weather(self, weather_data):
        # Clear previous weather display
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        if isinstance(weather_data, dict):
            labels = [
                f"City: {weather_data['city']}, {weather_data['country']}",
                f"Temperature: {weather_data['temperature']}°C",
                f"Feels like: {weather_data['feels_like']}°C",
                f"Conditions: {weather_data['description']}",
                f"Humidity: {weather_data['humidity']}%",
                f"Wind: {weather_data['wind_speed']} m/s"
            ]
            
            for text in labels:
                label = ttk.Label(self.weather_frame, text=text)
                label.pack()
            
            # Add to favorites button
            ttk.Button(self.weather_frame, text="Add to Favorites",
                      command=lambda: self.add_favorite(weather_data['city'])).pack(pady=10)
    
    def add_favorite(self, city):
        self.app.save_favorite(city)
        self.update_favorites_list()
        messagebox.showinfo("Success", f"Added {city} to favorites!")
    
    def update_favorites_list(self):
        # Add/update favorites display
        pass
    
    def run(self):
        self.root.mainloop()