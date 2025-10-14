# DataMerger.py

import flet as ft
import pandas as pd

import os



def main(page: ft.Page):
    ### Load and Read files
    def load_file(filepath: str, **kwargs) -> pd.DataFrame:
        ext = os.path.splitext(filepath)[1].lower()
        if ext in [".csv"]:
            df = pd.read_csv(filepath, **kwargs)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(filepath, **kwargs)
        elif ext in [".txt"]:
            df = pd.read_csv(filepath, sep="\t", **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        return df
    
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




### === RUN APP ===
ft.run(main)