# load_csv_gui.py

# === Imports ===
import pandas as pd
import flet as ft


# 読み込んだテキストデータを保持するためのグローバル変数
csv_text_data = []

# CSV Handlers
def setup_csv_loader(page):
    def file_handler(e: ft.FilePickerResultEvent):
        if e.files:
            csv_path = e.files[0].path
            try:
                df = pd.read_csv(csv_path)
                content = df["Content"].dropna().tolist()
                csv_text_data.clear()
                csv_text_data.extend(content)
                print("CSV loaded:", content) # debug用
            except Exception as err:
                print("Failed to load CSV. Error: ", err) # debug用

    file_picker = ft.FilePicker(on_result=file_handler)
    page.overlay.append(file_picker)

    open_button = ft.ElevatedButton(text="OPEN CSV", on_click=lambda e: file_picker.pick_files(allow_multiple=False))

    return open_button

# CSV Handle (to load stopwords) -> load_stopwordsは別にモジュールとして作る
