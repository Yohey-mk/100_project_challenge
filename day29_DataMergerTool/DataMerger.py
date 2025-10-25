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

    df_state = {
        "files": {}, # {"filename": DataFrame, ...}
        "merge_main": None,
        "merge_key": None,
        "sub_file": None,
        "sub_key": None,
    }

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
            
            setup_text.value = f"{len(files)} file(s) selected."
            df_state["files"].clear()
            for f in files:
                try:
                    df = load_file(f.path)
                    df_state["files"][f.name] = df
                except Exception as err:
                    setup_text.value = f"Failed to load {f.name}: {err}"
                    page.update()
                    return
            first_name = list(df_state["files"].keys())[0]
            update_table(df_state["files"][first_name], first_name)
            update_main_file_dropdown()
            update_sub_file_dropdown()
            page.update()

        open_button = ft.ElevatedButton(
            content=ft.Text("Open file(s)"),
            on_click=open_file_picker,
        )
        return ft.Column(controls=[open_button, setup_text])
    open_file_button = read_file(page)

    ### Table Management
    def build_file_list():
        file_list_column.controls.clear()
        if not df_state["files"]:
            file_list_column.controls.append(ft.Text("No files loaded."))
            return
        for name in df_state["files"].keys():
            btn = ft.TextButton(
                content=ft.Text(name),
                on_click=lambda e, n=name: update_table(df_state["files"][n], n),
            )
            file_list_column.controls.append(btn)
        page.update()

    def update_table(df: pd.DataFrame, name: str):
        table_placeholder.controls.clear()
        table_placeholder.controls.append(ft.Text(f"Preview : {name}", weight="bold"))
        table_placeholder.controls.append(preview_mode(df))
        build_file_list()
        page.update()

    def preview_mode(df: pd.DataFrame):
        import io
        buffer = io.StringIO()
        df.to_string(buffer, index=False)
        # scrollable text (Text -> wrap with row and column)
        text=ft.Text(
                buffer.getvalue(),
                selectable=True,
                size=12,
                font_family="monospace")
        scrollable_text = ft.Column(
            controls=[
                ft.Row(
                    controls=[text],
                    scroll=ft.ScrollMode.AUTO,
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        return scrollable_text

    def datatable_view(df: pd.DataFrame) -> ft.Container:
        if df.empty:
            return ft.Container(
                content=ft.Text("No data loaded."),
                padding=10,
            )

        header_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(col, weight="bold"),
                    width=70, padding=5,
                )
                for col in df.columns
            ],
            spacing=0,
        )

        data_rows = []
        for _, row in df.iterrows():
            r = ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(str(cell)),
                        width=150, padding=5,
                    )
                    for cell in row
                ],
                spacing=0
            )
            data_rows.append(r)

        vertical_list_view = ft.ListView(
            controls=data_rows,
            expand=True,
            auto_scroll=False,
            spacing=0,
            height=350,
        )

        horizontal_scrollable_table = ft.Column(
            controls=[header_row, vertical_list_view],
            scroll=ft.ScrollMode.ALWAYS,
            width=page.window.width * 0.45,
            height=400,
            expand=False,
        )

        return horizontal_scrollable_table

    ### Dropdown / Key select
    def update_main_file_dropdown():
        main_file_dropdown.options.clear()
        if not df_state["files"]:
            main_file_dropdown.options.append(ft.dropdown.Option("No files loaded"))
            main_file_dropdown.disabled = True
        else:
            for name in df_state["files"].keys():
                main_file_dropdown.options.append(ft.dropdown.Option(name))
            main_file_dropdown.disabled = False
        page.update()

    def main_file_changed(e):
        df_state["merge_main"] = e.control.value
        print(f"Main file selected: {df_state['merge_main']}")
        update_merge_key_dropdown()
        update_sub_file_dropdown()

    def update_merge_key_dropdown():
        merge_key_dropdown.options.clear()
        if not df_state.get("merge_main"):
            merge_key_dropdown.options.append(ft.dropdown.Option("No main file selected"))
            merge_key_dropdown.disabled = True
        else:
            df = df_state["files"][df_state["merge_main"]]
            for col in df.columns:
                merge_key_dropdown.options.append(ft.dropdown.Option(col))
            merge_key_dropdown.disabled = False
        page.update()

    def merge_key_changed(e):
        df_state["merge_key"] = e.control.value
        print(f"Merge key selected: {df_state['merge_key']}")

    def sub_file_selected(e):
        sub_filename = e.control.value
        df_state["sub_file"] = sub_filename
        df = df_state["files"][sub_filename]
        sub_key_dropdown.options = [ft.dropdown.Option(c) for c in df.columns]
        page.update()

    def sub_key_selected(e): #ここでMergeするサブキーを選択
        df_state["sub_key"] = e.control.value
        print(f"Sub key selected: {df_state['sub_key']}")

    def update_sub_file_dropdown():
        sub_file_dropdown.options.clear()
        if not df_state["files"]:
            sub_file_dropdown.options.append(ft.dropdown.Option("No files loaded"))
            sub_file_dropdown.disabled = True
        else:
            for name in df_state["files"].keys():
                if name != df_state.get("merge_main"):
                    sub_file_dropdown.options.append(ft.dropdown.Option(name))
            sub_file_dropdown.disabled = False
        page.update()

    ### Data Marger
    def merge_files(e):
        main_file = df_state.get("merge_main")
        sub_file = df_state.get("sub_file")
        main_key = df_state.get("merge_key")
        sub_key = df_state.get("sub_key")

        if not all([main_file, sub_file, main_key, sub_key]):
            print("Please select all merge parameters.")
            return
        
        df_main = df_state["files"][main_file]
        df_sub = df_state["files"][sub_file]

        # キーを文字列化（型不一致を防ぐ）
        df_main_copy = df_main.copy()
        df_sub_copy = df_sub.copy()
        try:
            df_main_copy[main_key] = df_main_copy[main_key].astype(str)
            df_sub_copy[sub_key] = df_sub_copy[sub_key].astype(str)
        except Exception as err:
            print(f"Type conversion failed: {err}")
            return

        # Merge Data
        try:
            merged_df = pd.merge(
                df_main_copy, df_sub_copy,
                left_on=main_key, right_on=sub_key,
                how="left"
            )
        except Exception as err:
            print(f"Merge failed: {err}")

        print(f"Merged {main_file} and {sub_file} using  {main_key} <-> {sub_key}")
        datatable_placeholder.content = datatable_view(merged_df)
        #update_table(merged_df, f"Merged {main_file} + {sub_file}")
        page.update()
    
    merge_button = ft.ElevatedButton("Merge files", on_click=merge_files)

    ### Table Containers
    file_list_column = ft.Column(scroll="auto", expand=True, tight=True)
    file_list_container = ft.Container(
        content=ft.Column(
            controls=[file_list_column],
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=100,
        width=500,
        padding=10,
    )
    table_placeholder = ft.Column(scroll="auto", expand=True, tight=True)
    table_container = ft.Container(
        content=ft.Column(
            controls=[table_placeholder],
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=300,
        width=500,
        padding=10,
    )

    datatable_placeholder = ft.Container(
        content=datatable_view(pd.DataFrame()),
        expand=True,
        height=400,
    )

    ### Layout
    # Left Card
    left_card = ft.Card(
        ft.Container(
            content=ft.Column([
                open_file_button,
                file_list_container,
                table_container,
            ], tight=True, spacing=8),
        )
    )

    # Right Card / Components
    main_file_dropdown = ft.Dropdown(
        label="Select Main File",
        options=[],
        on_change=main_file_changed,
        width=500,
        disabled=True,
    )

    merge_key_dropdown = ft.Dropdown(
        label="Select merge key",
        options=[],
        on_change=merge_key_changed,
        width=300,
        disabled=True
    )

    sub_file_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(f) for f in df_state["files"] if f != df_state["merge_main"]],
        on_change=sub_file_selected,
        width=300,
    )

    sub_key_dropdown = ft.Dropdown(on_change=sub_key_selected, width=300,)

    right_card = ft.Card(
        ft.Container(
            content=ft.Column([
                ft.Text("Main File Settings", weight="bold"),
                main_file_dropdown,
                merge_key_dropdown,
                ft.Divider(),
                ft.Text("Sub File Settings", weight="bold"),
                sub_file_dropdown,
                sub_key_dropdown,
                ft.Divider(),
                merge_button,
                datatable_placeholder,
            ], tight=True, spacing=8,),
        )
    )

    page.add(
        ft.Row(
            controls=[left_card,right_card],
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.START,
        )
    )


### === RUN APP ===
ft.run(main)