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
        user_input = input("Choose which item to edit\n1. Date / 2. Category / 3. Amount / 4. Memo: ")
        if user_input == "1" or user_input.lower() == "date":
            column = "Date"
            old_value = df.at[idx, column]
        elif user_input == "2" or user_input.lower() == "category":
            column = "Category"
            old_value = df.at[idx, column]
        elif user_input == "3" or user_input.lower() == "amount":
            column = "Amount"
            old_value = df.at[idx, column]
        elif user_input == "4" or user_input.lower() == "memo":
            column = "Memo"
            old_value = df.at[idx, column]
        #elif user_input not in df.columns:
        #    print("Invalid column.")
        #    return df
        else:
            print("Invalid column.")
            return df
        if column in ["Date", "Category", "Memo"]:
            new_value = input(f"Enter new value for {column}: ")
        elif column == "Amount":
            try:
                new_amount = input("Enter a new value: ")
                new_value = float(new_amount)
            except ValueError:
                print("Please enter valid numbers.")
                return df
        df.at[idx, column] = new_value
    print(f"Old value: {old_value}")
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
        user_edit(df, filtered_df)

        return df
