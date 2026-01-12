import tkinter as tk
from tkinter import ttk, messagebox


class WeatherGUI:
    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        self.root.title("🌍 Weather Dashboard")
        self.root.geometry("420x520")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # ================= HEADER ================= #
        header = ttk.Label(
            self.root,
            text="Weather Dashboard",
            font=("Segoe UI", 16, "bold")
        )
        header.pack(pady=10)

        # ================= SEARCH ================= #
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=5)

        ttk.Label(search_frame, text="City:").grid(row=0, column=0, padx=5)
        self.city_entry = ttk.Entry(search_frame, width=25)
        self.city_entry.grid(row=0, column=1, padx=5)
        self.city_entry.bind("<Return>", lambda e: self.get_weather())

        ttk.Button(
            search_frame,
            text="Get Weather",
            command=self.get_weather
        ).grid(row=0, column=2, padx=5)

        # ================= STATUS ================= #
        self.status_var = tk.StringVar(value="Ready")
        status = ttk.Label(self.root, textvariable=self.status_var)
        status.pack(pady=5)

        # ================= WEATHER DISPLAY ================= #
        self.weather_frame = ttk.LabelFrame(self.root, text="Current Weather")
        self.weather_frame.pack(padx=15, pady=10, fill="x")

        # ================= FAVORITES ================= #
        fav_frame = ttk.LabelFrame(self.root, text="⭐ Favorites")
        fav_frame.pack(padx=15, pady=10, fill="both", expand=True)

        self.fav_listbox = tk.Listbox(fav_frame, height=6)
        self.fav_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.fav_listbox.bind("<<ListboxSelect>>", self.load_favorite)

        self.update_favorites_list()

    # ================= LOGIC ================= #

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        self.status_var.set("Fetching weather...")
        self.root.update_idletasks()

        try:
            weather = self.app.get_current_weather(city)
            self.display_weather(weather)
            self.status_var.set("Done")
        except Exception as e:
            self.status_var.set("Error")
            messagebox.showerror("Error", str(e))

    def display_weather(self, weather):
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        if not isinstance(weather, dict):
            messagebox.showerror("Error", "Invalid weather data")
            return

        emoji = self.get_weather_emoji(weather["description"])

        ttk.Label(
            self.weather_frame,
            text=f"{emoji} {weather['city']}, {weather['country']}",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=5)

        details = [
            f"🌡 Temperature: {weather['temperature']}°C",
            f"🤔 Feels like: {weather['feels_like']}°C",
            f"☁️ Condition: {weather['description'].title()}",
            f"💧 Humidity: {weather['humidity']}%",
            f"💨 Wind: {weather['wind_speed']} m/s",
        ]

        for d in details:
            ttk.Label(self.weather_frame, text=d).pack(anchor="w", padx=10)

        ttk.Button(
            self.weather_frame,
            text="⭐ Add to Favorites",
            command=lambda: self.add_favorite(weather["city"])
        ).pack(pady=10)

    def add_favorite(self, city):
        self.app.save_favorite(city)
        self.update_favorites_list()
        messagebox.showinfo("Success", f"{city} added to favorites!")

    def update_favorites_list(self):
        self.fav_listbox.delete(0, tk.END)
        for city in self.app.load_favorites():
            self.fav_listbox.insert(tk.END, city)

    def load_favorite(self, event):
        selection = self.fav_listbox.curselection()
        if selection:
            city = self.fav_listbox.get(selection[0])
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, city)
            self.get_weather()

    # ================= UTILS ================= #

    def get_weather_emoji(self, desc):
        desc = desc.lower()
        if "rain" in desc:
            return "🌧️"
        if "cloud" in desc:
            return "☁️"
        if "clear" in desc:
            return "☀️"
        if "snow" in desc:
            return "❄️"
        if "storm" in desc:
            return "⛈️"
        return "🌡️"

    def run(self):
        self.root.mainloop()
