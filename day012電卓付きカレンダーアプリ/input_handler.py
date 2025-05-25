#input_handler.py
from datetime import datetime
import flet as ft #ModuleでFletを使うのでimportする必要あり

def get_user_input(on_submit_handler):
    return ft.TextField(
        label="Enter a date (yyyy-mm-dd)",
        hint_text="2025-01-01",
        on_submit=on_submit_handler
    )

def parse_date_input(date_str: str):
    return datetime.strptime(date_str, "%Y-%m-%d")