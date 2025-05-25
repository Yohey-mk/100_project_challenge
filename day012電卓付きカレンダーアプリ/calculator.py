#calculator.py
from datetime import timedelta

def date_calculation(base_date, new_days_offset):
    return base_date + timedelta(days = new_days_offset)