# home_expenses_book_gui.py

### === Imports ===
import flet as ft
import pandas as pd
import sys
import os
from datetime import datetime

from utils import load_csv, save_csv, on_save_clicked
from home_ui import back_home
from calendar_view import render_calendar_ui, open_day_editor


### === App Logics ===
def main(page: ft.Page):
    page.title = "Home Expenses Book Refined"
    page.scroll = "auto"
    expense_book = load_csv()
    #input_form_column = ft.Column()

    def on_submit_handler(entries):
        expense_book.append(entries)
        save_csv(expense_book)
        page.update()


### === UI Components ===
    #date_input_ui = ft.ElevatedButton(text="Input date", on_click=on_save_clicked)
    home_button = ft.ElevatedButton(text="HOME", on_click=lambda e: back_home(page))
    calendar_view = ft.ElevatedButton(
        text="Calendar",
        on_click=lambda e: render_calendar_ui(page, datetime.now().year, datetime.now().month))
    home_ui = ft.Row(controls=[home_button], alignment="center")
    calendar_ui = ft.Row(controls=[calendar_view], alignment="center")
    home_msg = ft.Text("WELCOME TO HOME EXPENSE BOOK REFINED!")
    home_msg_ui = ft.Row(controls=[home_msg], alignment="center")
    show_today_editor = ft.ElevatedButton(text="TODAY", on_click=lambda e: open_day_editor(page, datetime.now().year, datetime.now().month, datetime.now().day))
    show_today_editor_ui = ft.Row(controls=[show_today_editor], alignment="center")
### === UI Interfaces ===
    page.add(
        home_msg_ui,
        ft.Divider(),
        home_ui,
        calendar_ui,
        show_today_editor_ui,
        ft.Divider()
        )
    page.update()

### === Run App ===
ft.app(target=main)