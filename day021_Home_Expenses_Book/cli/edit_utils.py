# edit_expenses.py
import pandas as pd
from show_list import show_list
from utils import get_valid_date

def user_edit(df, target_df=None):
    target = target_df if target_df is not None else df
    try:
        idx = int(input("Choose which one to edit: "))
        if idx not in target.index:
            print("Invalid index.")
            return df
    except ValueError:
        print("Please enter a valid number.")
        return df
    else:
        column = input("Choose which item to edit(Date/Category/Amount/Memo): ")
        if column not in df.columns:
            print("Invalid column.")
            return df
        new_value = input(f"Enter new value for {column}: ")
        if column == "Amount":
            new_value = float(new_value)
        df.at[idx, column] = new_value
    print(f"{column} has been updated to {new_value}")
    return df

def edit_list(df):
    print("1. Choose from all list\n2. Search by date")
    edit_option = input("Choose edit option: ")
    if edit_option == "1":
        show_list(df)
        user_edit(df)
        return df

    elif edit_option == "2":
        date_to_search = get_valid_date() #Dateで探して、一致するもののみをフィルタして表示？
        filtered_df = df[df["Date"] == date_to_search]

        if filtered_df.empty:
            print("No entries found.")
            return df
        print(filtered_df)
        user_edit(df)

        return df
