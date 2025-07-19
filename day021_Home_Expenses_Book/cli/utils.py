# utils.py

import os
import sys
import pandas as pd

# handle_csvみたいなモジュール化してそこにまとめてもいいかも
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys.MEIPASS, filename)

def load_csv(filename="day21_CLI.csv"):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Memo"])

def save_csv(df, filename="day21_CLI.csv"):
    df.to_csv(filename, index=False)

def get_valid_date():
    while True:
        print("*Press Q to quit")
        date_str = input("Enter a date(YYYY-MM-DD): ")
        if date_str.lower() == "q":
            break
        try:
            pd.to_datetime(date_str)
            return date_str
        except ValueError:
            print("Invalid Input. Please enter again.")