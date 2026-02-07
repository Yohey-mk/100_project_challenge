# api_weather_app.py

import requests
import json

# 1. APIのエンドポイント（窓口のURL）
url = "https://api.open-meteo.com/v1/forecast"

# 2. パラメータの設定
# 東京の座標を指定
tokyo_params = {
    "latitude": 35.6895,
    "longitude": 139.6917,
    "current_weather": True,
    "timezone": "Asia/Tokyo"
}

# Californiaの座標を指定
ca_pramas = {
    "latitude": 36.7783,
    "longitude": 119.4179,
    "current_weather": True,
    "timezone": "PST"
}

print("天気情報を取得中...")

# 3. APIにリクエストを送る
# params=paramsとすることで、URLの後ろに自動で ?latitude=...とつける
tokyo_response = requests.get(url, params=tokyo_params)
ca_response = requests.get(url, params=ca_pramas)

# 4. 返ってきたJSONデータをPythonの辞書に変換する
tokyo_data = tokyo_response.json()
ca_data = ca_response.json()

# Debug: データの中身を綺麗に表示してみる
# print(json.dumps(ca_data, indent=2))

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

# 5. 必要な情報を取り出す
tyo_current = tokyo_data["current_weather"]
tyo_current_time = tyo_current["time"]
tyo_temperature = tyo_current["temperature"]
tyo_windspeed = tyo_current["windspeed"]
tyo_weather_code = tyo_current["weathercode"]
tyo_weather_name = weather_dict.get(tyo_weather_code, "Other")

ca_current = ca_data["current_weather"]
ca_current_time = ca_current["time"]
ca_temperature = ca_current["temperature"]
ca_windspeed = ca_current["windspeed"]
ca_weather_code = ca_current["weathercode"]
ca_weather_name = weather_dict.get(ca_weather_code, "Other")

print("\n--- 東京 / Californiaの天気 ---")
print(f"時刻: {tyo_current_time} / {ca_current_time}")
print(f"気温; {tyo_temperature} / {ca_temperature}")
print(f"風速: {tyo_windspeed} / {ca_windspeed}")
print(f"天気: {tyo_weather_name} / {ca_weather_name}")