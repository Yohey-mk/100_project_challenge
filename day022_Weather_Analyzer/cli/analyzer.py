# analyzer.py
import pandas as pd
from pandas.tseries.offsets import MonthEnd

def show_summary(df):
    print("Data summary:")
    print(df.describe())

def analyze_temperature_trend(df):
    print("Temperature trend")
    print(df[["Date", "Temperature"]].head())

def show_specific_trend(df):
    selected_date_range_start = input("Enter a start date(YYYY-MM): ")
    selected_date_range_end = input("Enter an end date(YYYY-MM): ")

    start_date = pd.to_datetime(selected_date_range_start + "-01")
    end_date = pd.to_datetime(selected_date_range_end + "-01") + MonthEnd(0)

    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    #filtered_df_fnl = filtered_df[filtered_df["Date"] <= selected_date_range_end]
    print(filtered_df[["Date", "Temperature"]].head())
    print(filtered_df.describe())
    return filtered_df