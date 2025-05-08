import requests
import jmespath


class WeatherService:
    weather_icons = {
        "Sunny": "☀️",
        "Clear": "🌙",
        "Partly cloudy": "⛅",
        "Cloudy": "☁️",
        "Overcast": "🌥️",
        "Mist": "🌫️",
        "Patchy rain possible": "🌦️",
        "Light rain": "🌧️",
        "Heavy rain": "🌧️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Fog": "🌁",
    }

    def __init__(self, city):
        self.city = city

    def fetch_weather(self):
        url = f"https://wttr.in/{self.city}?format=j1"
        try:
            response = requests.get(url)
            data = response.json()
            temp = jmespath.search('current_condition[0].temp_C', data)
            weather_desc = jmespath.search('current_condition[0].weatherDesc[0].value', data)
            city_name = jmespath.search('nearest_area[0].areaName[0].value', data)
            icon = self.weather_icons.get(weather_desc, "❔")
            return temp, icon, city_name
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather: {e}")
            return None, None, self.city
