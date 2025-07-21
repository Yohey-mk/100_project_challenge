# home_expenses_book_gui.py

### === Imports ===
import flet as ft
import pandas as pd
import sys
import os

from utils import load_csv, save_csv, on_save_clicked


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

    date_input_ui = ft.ElevatedButton("Input date", on_click=show_date_input)

### === UI Interfaces ===
    page.add(date_input_ui)
    page.update()

### === Run App ===
ft.app(target=main)