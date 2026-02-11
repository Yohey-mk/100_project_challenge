# api_weather_flet.py

import requests
import flet as ft

def main(page: ft.Page):
    page.title = "Weather App"
    page.window.height = 1000
    page.window.width = 700
    page.scroll = ft.ScrollMode.AUTO
    
    city_name = ft.TextField(label="Enter a city name", width=300)
    latitude = ft.TextField(label="Enter the latitude", width=300, value="35.6895")
    longitude = ft.TextField(label="Enter the longitude", width=300, value="139.6917")
    time_zone = ft.TextField(label="Enter the timezone", width=300, value="Asia/Tokyo")

    # Weather Interpretation Codes
    weather_dict = {
        0: "快晴 ☀️",
        1: "晴れ 🌤",
        2: "一部曇り ⛅️",
        3: "曇り ☁️",
        45: "霧 🌫",
        51: "霧雨 🌧",
        61: "雨 ☔️",
        71: "雪 ☃️",
        95: "雷雨 ⚡️"
    }

    result_field = ft.Text(width=400, height=500)

    def get_weather(e):
        cityname = city_name.value
        lat = latitude.value
        lon = longitude.value
        timezone = time_zone.value
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "city": cityname,
            "latitude": lat,
            "longitude": lon,
            "timezone": timezone,
            "current_weather": True
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            current = data["current_weather"]
            weather_code = current["weathercode"]
            weather_str = weather_dict.get(weather_code, "Other")

            result_field.value = (
                f"City: {cityname}\n"
                f"Time: {current['time']}\n"
                f"Temperature: {current['temperature']}\n"
                f"Windspeed: {current['windspeed']}\n"
                f"Weather: {weather_str}"
                )
            
        except Exception as err:
            result_field.value = f"Error: {err}"
            result_field.color = ft.Colors.RED
        
        page.update()

    run_get_weather_btn = ft.Button(content="Get Weather", on_click=get_weather)
    

    page.add(
        city_name,
        latitude,
        longitude,
        time_zone,
        run_get_weather_btn,
        ft.Divider(),
        result_field
    )

ft.run(main)