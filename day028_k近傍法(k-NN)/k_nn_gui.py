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
from train_test_split import get_dfs, train_test_split_by_user, UserBasedRecommender, ItemBasedRecommender, precision_at_k, mean_precision_at_k

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

    df_state = {"df": None}

    ### UI Components
    # pics
    img_view = ft.Image(src_base64=EMPTY_IMAGE, width=640, height=400, fit=ft.BoxFit.CONTAIN)

    # Pick User/Item Based Analyzer
    user_item_based_picker = ft.Dropdown(label="Choose User/Item Based Analyzer", 
                                         options=[ft.dropdown.Option("User-Based"),
                                                  ft.dropdown.Option("Item-Based")], 
                                                  value="User-Based", width=250)

    # Input fields
    #choose_user_or_item_id = ft.TextField(value="1", label="Pick User/Item ID", 
    #                                      on_change=lambda e: run_data_analysis(page, df_state))
    top_n_input = ft.TextField(value="1", label="Show how many recommended item(s)")


    ### Setup Functions
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
                setup_text.value = f"File Loaded: {f.name}."
                preview_dataframe(page, df_state)
            except Exception as err:
                setup_text.value = f"Failed to load file(s): {err}"
            page.update()
        open_button = ft.ElevatedButton(
            content=ft.Text("Open file(s)"),
            on_click=open_file_picker,
        )
        return ft.Column(controls=[open_button, setup_text])
    open_file_button = read_file(page)
            
    def preview_dataframe(page: ft.Page, df_state):
        columns = [ft.DataColumn(ft.Text(col)) for col in df_state["df"].columns]
        rows = []
        for _, row in df_state["df"].head(10).iterrows():
            cells = [ft.DataCell(ft.Text(str(val))) for val in row]
            rows.append(ft.DataRow(cells=cells))
        table = ft.DataTable(columns=columns, rows=rows)
        page.add(table)

    # Data Analysis based on user/item choice
    def run_data_analysis(page: ft.Page, df, user_or_item_id):
        if df_state["df"] is None:
            return
        
        user_or_item_id = str(user_or_item_id).strip()
        if not user_or_item_id:
            return
        
        df = df_state["df"]
        item_master_df = df.drop_duplicates("item_id")[["item_id", "sex", "age", "type", "color"]].reset_index(drop=True)

        if user_item_based_picker.value == "User-Based":
            page.add(ft.Text(f"User-based analysis for ID {user_or_item_id}"))
            train_df, test_df = train_test_split_by_user(df, test_size=0.2)
            recommender = UserBasedRecommender(train_df, item_master_df, n_neighbors=6)
            try:
                recs = recommender.recommend(user_id=int(user_or_item_id), top_k=5, with_attributes=True)
                print(recs)
                recommends_columns = [ft.DataColumn(ft.Text(col)) for col in recs.columns]
                recommends_rows = []
                for _, row in recs.iterrows():
                    cells = [ft.DataCell(ft.Text(str(val))) for val in row]
                    recommends_rows.append(ft.DataRow(cells=cells))
                recommends_table = ft.DataTable(columns=recommends_columns, rows=recommends_rows)

                page.controls = [c for c in page.controls if not isinstance(c, ft.DataTable)]
                page.add(recommends_table)
                page.update()
            except Exception as err:
                print(f"Error during recommendation: {err}")
        elif user_item_based_picker.value == "Item-Based":
            page.add(ft.Text(f"Item-based analysis for ID {user_or_item_id}"))
        page.update()

    choose_user_or_item_id = ft.TextField(
        value="1",
        label="Pick User/Item ID",
        on_change=lambda e: run_data_analysis(page, df_state, e.control.value)
    )

    ### Layout
    page.add(
        user_item_based_picker,
        open_file_button,
        ft.Divider(),
        choose_user_or_item_id,
        top_n_input,
    )

### === RUN APP ===
ft.run(main)