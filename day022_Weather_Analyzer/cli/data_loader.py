# data_loader.py

import pandas as pd

def load_weather_data(path):
    df = pd.read_csv(path, encoding="utf-8")
    df["Date"] = pd.to_datetime(df["Date"])
    return df