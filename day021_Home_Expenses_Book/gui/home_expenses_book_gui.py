# home_expenses_book_gui.py

### === Imports ===
import flet as ft
import pandas as pd
import sys
import os
from datetime import datetime

from utils import load_csv, save_csv, on_save_clicked
from home_ui import back_home
from calendar_view import render_calendar_ui


### === App Logics ===
def main(page: ft.Page):
    page.title = "Home Expenses Book Refined"
    page.scroll = "auto"
    expense_book = load_csv()

    def on_submit_handler(entries):
        expense_book.append(entries)
        save_csv(expense_book)
        page.update()


### === UI Components ===
    def show_date_input(e):
        on_save_clicked(page)

    date_input_ui = ft.ElevatedButton(text="Input date", on_click=show_date_input)
    home_button = ft.ElevatedButton(text="HOME", on_click=lambda e: back_home(page))
    calendar_view = ft.ElevatedButton(
        text="Calendar",
        on_click=lambda e: render_calendar_ui(page, datetime.now().year, datetime.now().month))

### === UI Interfaces ===
    page.add(
        date_input_ui,
        home_button,
        calendar_view
        )
    page.update()

### === Run App ===
ft.app(target=main)