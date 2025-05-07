#calculator.py
from datetime import datetime, timedelta

def date_calculation(base_date):
    input_new_date = int(input("Enter how many days before / after you want to know: "))
    new_date_result = base_date + timedelta(input_new_date)
    return new_date_result
