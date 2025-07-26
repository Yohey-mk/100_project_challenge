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

def on_save_clicked(e):
    page = e.page

    input_form_column = page.controls[3]

    date_input = ft.TextField(label="(YYYY-MM-DD)")
    category_input = ft.TextField(label="Category")
    amount_input = ft.TextField(label="Amount")
    memo_input = ft.TextField(label="Memo")

    #expense_book = load_csv()

    def on_submit(submit_event):
        try:
            pd.to_datetime(date_input.value)
            amount = int(amount_input.value)
            entry = {
                "Date": date_input.value,
                "Category": category_input.value,
                "Amount": amount,
                "Memo": memo_input.value
            }
            #expense_book.loc[len(expense_book)] = entry
            df = load_csv()
            df.loc[len(df)] = entry
            save_csv(df)
            input_form_column.controls.append(ft.Text("saved!"))
            #save_csv(expense_book)
            #page.controls.clear()
            #refresh_page()
            #page.add(ft.Text("Saved!"))
        except ValueError as err:
            input_form_column.controls.append(ft.Text(f"{err}. Please try again."))
            #page.add(ft.Text(f"{err}. Please try again."))
        input_form_column.update()
    
    input_form_column.controls.clear()
    input_form_column.controls.extend([
        date_input,
        category_input,
        amount_input,
        memo_input,
        ft.ElevatedButton(text="Save", on_click=on_submit)
    ])
    input_form_column.update()


    #def refresh_page():
    #    page.controls.clear()
    #    on_save_clicked(page)
    #    date_input.value = ""
    #    category_input.value = ""
    #    amount_input.value = ""
    #    memo_input.value = ""
    #    page.update()
    #
    #save_button = ft.ElevatedButton(text="Save", on_click=on_submit)
    #
    #page.add(
    #    date_input,
    #    category_input,
    #    amount_input,
    #    memo_input,
    #    save_button
    #)
    #page.update()