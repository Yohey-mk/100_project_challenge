# utils,py

import os
import sys
import pandas as pd
import flet as ft

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys.MEIPASS, filename)
    
def load_csv(filename="dat21_guI.csv"):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Memo"])
    
def save_csv(df, filename="day21_GUI.csv"):
    df.to_csv(filename, index=False)

def get_valid_date():
    quit_howto_msg = ft.Text("*Press Q to quit")
    date_input_field = ft.TextField(label="Enter a date(YYYY-MM-DD)")