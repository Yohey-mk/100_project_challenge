# load_stopwords_gui.py

### === Imports ===
import pandas as pd
import flet as ft


csv_stopwords_gui = []

# Stopwords Handler
def setup_stopwords(page):
    def file_handler(e: ft.FilePickerResultEvent):
        if e.files:
            csv_path = e.files[0].path
            try:
                df = pd.read_csv(csv_path)
                content = df["Stopwords"].dropna().tolist()
                csv_stopwords_gui.clear()
                csv_stopwords_gui.extend(content)
                print("csv loaded", content)
            except Exception as err:
                print("load failed. Error:", err)

    file_picker = ft.FilePicker(on_result=file_handler)
    page.overlay.append(file_picker)

    open_stopwords_button = ft.ElevatedButton(text="Set stopwords", on_click=lambda e:file_picker.pick_files(allow_multiple=False))

    return open_stopwords_button