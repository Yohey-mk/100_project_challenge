# DataMerger.py

import flet as ft
import pandas as pd

import os



def main(page: ft.Page):
    ### Initial Setup
    page.title = "Data Merger"
    page.scroll = "auto"
    page.window.width = 1200
    page.window.height = 720

    df_state = {"df": None}

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
            try:
                df_state["df"] = load_file(f.path)
                setup_text.value = f"File loaded: {f.name}"
                update_table(df_state["df"])
            except Exception as err:
                setup_text.value = f"Failed to load file(s): {err}"
            page.update()
        open_button = ft.ElevatedButton(
            content=ft.Text("Open file(s)"),
            on_click=open_file_picker,
        )
        return ft.Column(controls=[open_button, setup_text])
    open_file_button = read_file(page)

    ### Table Management
    def update_table(df: pd.DataFrame):
        table_placeholder.controls.clear()
        table_placeholder.controls.append(preview_mode(df_state["df"]))
        page.update()

    def preview_mode(df: pd.DataFrame):
        import io
        buffer = io.StringIO()
        df.to_string(buffer, index=False)
        return ft.Text(
            buffer.getvalue(),
            selectable=True,
            size=12,
            font_family="monospace"
        )

    table_placeholder = ft.Column(scroll="auto", expand=True, tight=True)
    table_container = ft.Container(
        content=ft.Column(
            controls=[table_placeholder],
            scroll="auto",
        ),
        height=300,
        width=500,
        padding=10,
    )


    ### Layout
    page.add(
        open_file_button,
        table_container,
    )


### === RUN APP ===
ft.run(main)