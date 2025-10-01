# k_nn_gui.py
import io
import base64
import os

import flet as ft
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder

### === prior preps ===
EMPTY_IMAGE = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgkL5Bp8AAAAASUVORK5CYII="
)






# === Flet App ===
def main(page: ft.Page):
    page.title = "K-NN Analyzer"
    page.scroll = "auto"
    page.window.width = 1200
    page.window.height = 720

    ### UI Components
    # pics
    img_view = ft.Image(src_base64=EMPTY_IMAGE, width=640, height=400, fit=ft.BoxFit.CONTAIN)

    # Pick User/Item Based Analyzer
    user_item_based_picker = ft.Dropdown(label="Choose User/Item Based Analyzer", 
                                         options=[ft.dropdown.Option("User-Based"),
                                                  ft.dropdown.Option("Item-Based")], value="User-Based", width=250)

    ### Setup Functions
    def load_file(filepath: str, **kwargs) -> pd.DataFrame:
        ext = os.path.splitext(filepath)[1].lower()
        if ext in [".csv"]:
            return pd.read_csv(filepath, **kwargs)
        elif ext in [".xls", ".xlsx"]:
            return pd.read_excel(filepath, **kwargs)
        elif ext in [".txt"]:
            return pd.read_csv(filepath, sep="\t", **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
    def read_file(page: ft.Page):
        setup_text = ft.Text()
        file_picker = ft.FilePicker()
        page.services.append(file_picker)
        async def open_file_picker(e: ft.Event[ft.ElevatedButton]):
            files = await file_picker.pick_files(allow_multiple=True)
            try:
                f = files[0]
            except Exception:
                setup_text.value = "Canceled to load file(s)."
            try:
                df = load_file(f.path)
                setup_text.value = f"File Loaded: {f.name}."
            except Exception as err:
                setup_text.value = f"Failed to load file(s): {err}"
            page.update()
        open_button = ft.ElevatedButton(
            content=ft.Text("Open file(s)"),
            on_click=open_file_picker,
        )
        return ft.Column(controls=[open_button, setup_text])
    open_file_button = read_file(page)
            


    ### Layout
    page.add(
        user_item_based_picker,
        open_file_button,
    )

### === RUN APP ===
ft.run(main)