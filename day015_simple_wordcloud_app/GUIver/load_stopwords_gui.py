# load_stopwords_gui.py

# === Imports ===
import pandas as pd
import flet as ft


# CSV Handlers
def csv_handler(e):
    def open_handler(e):
        file_picker.pick_files(allow_multiple=False)

    def file_handler(e: ft.FilePickerResultEvent):
        if e.files:
            csv_path = e.files[0].path
        


# Buttons
    open_button = ft.ElevatedButton(label="OPEN", on_click=open_handler)
    file_picker = ft.FilePicker(on_result=file_handler)
    page.overlay.append(file_picker)


def load_stopwords(csv_file="stopwords.csv"):
    try:
        df = pd.read_csv(csv_file)
        stopwords = df["stopwords"].dropna().tolist()
        return stopwords
    except FileNotFoundError:
        print("No such file exists.")
        return []
    

def csv_reader():
    try:
        set_csv_file = input("enter the file name")
        df = pd.read_csv(f"{set_csv_file}.csv")
        text_column = df["Content"].dropna().tolist()
        return text_column
    except FileNotFoundError:
        return print("Couldn't read the csv file.")
    

# UI