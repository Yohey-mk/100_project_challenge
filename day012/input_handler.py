#input_handler.py
from datetime import datetime, timedelta

def get_user_input():
    date_input = input("enter a date(yyyy-mm-dd): ")
    base_date = datetime.strptime(date_input, "%Y-%m-%d")
    return base_date