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
    # preview table
    table_placeholder = ft.Column(scroll="auto", expand=True, tight=True)
    analysis_placeholder = ft.Column(scroll="auto", expand=True)
    table_container = ft.Container(
        content=ft.Column(
            controls=[table_placeholder],
            scroll="auto"
        ),
        height=300,
        width=500,
        padding=10,
    )
    #page.add(ft.Text("Data Preview"), table_placeholder)
    #page.add(ft.Text("Analysis Result"), analysis_placeholder)

    # functions related for tables
    def create_table(df: pd.DataFrame):
        return ft.DataTable(
            column_spacing=20,
            data_row_max_height=40,
            columns=[ft.DataColumn(ft.Text(col)) for col in df.columns],
            rows=[
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(val))) for val in row]
                ) for row in df.values.tolist()
            ]
        )
    def update_table(df: pd.DataFrame):
        table_placeholder.controls.clear()
        #table_placeholder.controls.append(create_table(df))
        table_placeholder.controls.append(preview_text_mode(df_state["df"]))
        page.update()

    # Pick User/Item Based Analyzer
    user_item_based_picker = ft.Dropdown(label="Choose User/Item Based Analyzer", 
                                         options=[ft.dropdown.Option("User-Based"),
                                                  ft.dropdown.Option("Item-Based")], 
                                                  value="User-Based", width=250)

    # Input fields
    #choose_user_or_item_id = ft.TextField(value="1", label="Pick User/Item ID", 
    #                                      on_change=lambda e: run_data_analysis(page, df_state))
    top_n_input = ft.TextField(value="1", label="Show how many recommended item(s)",
                               on_change=lambda e: run_data_analysis(page, df_state, e.control.value))

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
                update_table(df_state["df"])
                #preview_dataframe(page, df_state)
            except Exception as err:
                setup_text.value = f"Failed to load file(s): {err}"
            page.update()
        open_button = ft.ElevatedButton(
            content=ft.Text("Open file(s)"),
            on_click=open_file_picker,
        )
        return ft.Column(controls=[open_button, setup_text])
    open_file_button = read_file(page)
            
    def preview_text_mode(df: pd.DataFrame, max_rows=100):
        """DataFrameをテキスト表示（軽量化）"""
        import io
        buffer = io.StringIO()
        df.head(max_rows).to_string(buffer, index=False)
        return ft.Text(
            buffer.getvalue(),
            selectable=True,
            size=12,
            font_family="monospace"
        )

    # Data Analysis based on user/item choice
    def run_data_analysis(page: ft.Page, df, user_or_item_id):
        if df_state["df"] is None:
            return
        
        user_or_item_id = str(user_or_item_id).strip()
        if not user_or_item_id:
            return
        
        df = df_state["df"]
        item_master_df = df.drop_duplicates("item_id")[["item_id", "sex", "age", "type", "color"]].reset_index(drop=True)
        item_master_df["item_id"] = item_master_df["item_id"].astype(str)
        
        # Clear data placeholder
        analysis_placeholder.controls.clear()

        try:
            if user_item_based_picker.value == "User-Based":
                analysis_placeholder.controls.append(ft.Text(f"User-based analysis for ID {user_or_item_id}"))
                train_df, test_df = train_test_split_by_user(df, test_size=0.2)
                recommender = UserBasedRecommender(train_df, item_master_df, n_neighbors=6)
                # 型を合わせる
                user_id = str(user_or_item_id).strip()
                recs = recommender.recommend(user_id=user_id, top_k=int(top_n_input.value), with_attributes=True)
                print(recs)

                if isinstance(recs, list) or recs is None or len(recs) == 0:
                    analysis_placeholder.controls.append(
                        ft.Text(f"No Recommendations found for User ID '{user_id}")
                    )

                #recommends_columns = [ft.DataColumn(ft.Text(col)) for col in recs.columns]
                #recommends_rows = []
                #for _, row in recs.iterrows():
                #    cells = [ft.DataCell(ft.Text(str(val))) for val in row]
                #    recommends_rows.append(ft.DataRow(cells=cells))
                #recommends_table = ft.DataTable(columns=recommends_columns, rows=recommends_rows)
                else:
                    recommends_table = create_table(recs)
                #page.controls = [c for c in page.controls if not isinstance(c, ft.DataTable)]
                #page.add(recommends_table)
                    analysis_placeholder.controls.append(recommends_table)
                page.update()
            elif user_item_based_picker.value == "Item-Based":
                df_items = df_state["df"]
                all_items = df_items["item_id"].astype(str).unique().tolist()
                if user_or_item_id not in all_items:
                    analysis_placeholder.controls.append(
                        ft.Text(f"Item ID '{user_or_item_id}' not fount in dataset.")
                    )
                    page.update()
                    return
                analysis_placeholder.controls.append(ft.Text(f"Item-Based analysis for ID {user_or_item_id}"))
                recommender = ItemBasedRecommender(item_master_df, n_neighbors=6)
                # 型を合わせる
                user_purchased = [x.strip() for x in str(user_or_item_id).split(",") if x.strip()]
                user_purchased = [str(x) for x in user_purchased]
                recs = recommender.recommend(user_purchased=user_purchased, top_k=int(top_n_input.value), with_attributes=True)
                print(recs)
                recommend_table = create_table(recs)
                analysis_placeholder.controls.append(recommend_table)
                page.update()
        except Exception as err:
            analysis_placeholder.controls.append(ft.Text(f"Error during recommendation: {err}"))
        page.update()

    choose_user_or_item_id = ft.TextField(
        value="1",
        label="Pick User/Item ID",
        on_change=lambda e: run_data_analysis(page, df_state, e.control.value)
    )

    ### Layout
    left_card = ft.Card(
        ft.Container(
            content=ft.Column([
                user_item_based_picker,
                open_file_button,
                table_container,
            ]),
            padding=12, 
            margin=10,
            expand=True,
        )
    )

    right_card = ft.Card(
        ft.Container(
            content=ft.Column([
                choose_user_or_item_id,
                top_n_input,
                ft.Text("Analysis Result"),
                analysis_placeholder,
                ]),
                padding=12, 
                margin=10,
                expand=True,
        )
    )

    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(left_card, col={"xs": 12, "md": 4, "lg": 6}),
                ft.Container(right_card, col={"xs": 12, "md": 8, "lg": 6}),
            ],
            #user_item_based_picker,
            #pen_file_button,
            #choose_user_or_item_id,
            #top_n_input,
            
            #vertical_alignment=ft.CrossAxisAlignment.START,
            #alignment=ft.MainAxisAlignment.START,
            #expand=True,
    ))

### === RUN APP ===
ft.run(main)