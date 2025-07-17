# add_expenses.py

import pandas as pd

def add_expenses(df, date):
    category = input("Enter a category: ")
    amount = input("Enter a expenses: ")
    memo = input("Enter a note if applicable: ")

    new_row = pd.DataFrame([{
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Memo": memo
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    
    return df