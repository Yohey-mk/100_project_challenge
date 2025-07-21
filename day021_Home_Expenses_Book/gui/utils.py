# utils,py

import os
import sys
import pandas as pd
import flet as ft

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys.MEIPASS, filename)
    
def load_csv(filename="day21_gui.csv"):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Memo"])
    
def save_csv(df, filename="day21_gui.csv"):
    df.to_csv(filename, index=False)

def on_save_clicked(page: ft.Page):
    date_input = ft.TextField(label="(YYYY-MM-DD)")
    category_input = ft.TextField(label="Category")
    amount_input = ft.TextField(label="Amount")
    memo_input = ft.TextField(label="Memo")

    expense_book = load_csv()

    def on_submit(e):
        try:
            pd.to_datetime(date_input.value)
            amount = int(amount_input.value)
            entry = {
                "Date": date_input.value,
                "Category": category_input.value,
                "Amount": amount,
                "Memo": memo_input.value
            }
            expense_book.loc[len(expense_book)] = entry
            save_csv(expense_book)
            #page.controls.clear()
            refresh_page()
            page.add(ft.Text("Saved!"))
        except ValueError as err:
            page.add(ft.Text(f"{err}. Please try again."))

        page.update()

    def refresh_page():
        date_input.value = ""
        category_input.value = ""
        amount_input.value = ""
        memo_input.value = ""

    save_button = ft.ElevatedButton(text="Save", on_click=on_submit)

    page.add(
        date_input,
        category_input,
        amount_input,
        memo_input,
        save_button
    )
    page.update()