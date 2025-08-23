# linear_regression_gui.py

### === Imports ===
import flet as ft
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
import io

### === Functions ===
#モデルの作成と学習
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

EMPTY_IMAGE = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgkL5Bp8AAAAASUVORK5CYII="
)

### === App Logics ===
def main(page: ft.Page):
    page.title = "Linear Regression (Study hours -> Score)"
    page.scroll = "auto"

    # UI Components
    result_text = ft.Text(value="Upload a CSV file to start.", size=16)
    coef_text = ft.Text("")
    intercept_text = ft.Text("")
    pred_text =ft.Text("")
    image = ft.Image(src_base64=EMPTY_IMAGE)
    input_field = ft.TextField(label="Enter study hours(comma separated)", width=300)

    state = {"df": None, "model": None, "x_col": None, "y_col": None}

    # Dropdowns for column selection
    x_dropdown = ft.Dropdown(label="Select feature (X)", options=[], width=250)
    y_dropdown = ft.Dropdown(label="Select target (y)", options=[], width=250)

    def train(e):
        df = state["df"]
        if df is None:
            result_text.value = "No data loaded!"
            page.update()
            return
        
        if not x_dropdown.value or not y_dropdown.value:
            result_text.value = "Please select both X and y columns."
            page.update()
            return
        
        try:
            # X = np.array(df["study_hours"]).reshape(-1, 1)
            X = np.array(df[x_dropdown.value]).reshape(-1, 1) # study_hoursの部分にdropdownに入れる
            y = np.array(df[y_dropdown.value])
        except Exception as err:
            result_text.value = f"Error using selected columns: {err}"
            page.update()
            return

        model = train_model(X, y)
        state["model"] = model
        state["X"] = X
        state["y"] = y

        result_text.value = "Model trained successfully!"
        coef_text.value = f"Coefficient (slope): {model.coef_[0]:.2f}"
        intercept_text.value = f"Intercept: {model.intercept_:.2f}"

        # Base Plot

        fig, ax = plt.subplots()
        ax.scatter(X, y, color="blue", label="Training Data")
        ax.plot(X, model.predict(X), color="red")
        ax.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        image.src_base64 = base64.b64encode(buf.read()).decode("utf-8")

        page.update()

    def predict(e):
        model = state["model"]
        if model is None:
            pred_text.value = "Train the model first!"
        else:
            try:
                values = [float(x.strip()) for x in input_field.value.split(",")]
                X_new = np.array(values).reshape(-1, 1)
                y_pred = model.predict(X_new)
                pred_text.value = f"Predictions: {y_pred}"

                # Re-draw with predictions included
                X, y = state["X"], state["y"]
                fig, ax = plt.subplots()
                ax.scatter(X, y, color="blue", label="Training Data")
                ax.plot(X, model.predict(X), color="red", label="Regression line")
                ax.scatter(X_new, y_pred, color="green", marker="p", s=100, label="Predictions")
                ax.legend()

                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                plt.close(fig)
                buf.seek(0)
                image.src_base64 = base64.b64encode(buf.read()).decode("utf-8")
                page.update()
            except ValueError:
                pred_text.value = "Invalid input!"
        page.update()

    def csv_loader(page: ft.Page):
        setup_text = ft.Text()
        file_picker = ft.FilePicker()
        page.services.append(file_picker)

        async def open_file_picker(e: ft.Event[ft.ElevatedButton]):
            files = await file_picker.pick_files(allow_multiple=False)
            if not files:
                setup_text.value = "Canceled to select csv."
                page.update()
                return
            
            f = files[0]

            if not f.path:
                setup_text.value = "Web実行ではフルパス実行不可。アップロードAPIが必要です。"
                page.update()
                return
            
            try:
                df = pd.read_csv(f.path)
                state["df"] = df
                setup_text.value = f"CSV Loaded: {f.name} ({len(df)}件)"

                # 列名をドロップダウンに反映
                x_dropdown.options = [ft.dropdown.Option(col) for col in df.columns]
                y_dropdown.options = [ft.dropdown.Option(col) for col in df.columns]
                x_dropdown.value = None
                y_dropdown.value = None

            except Exception as err:
                setup_text.value = f"Failed to load CSV: {err}"

            page.update()

        open_button = ft.ElevatedButton(
            content=ft.Text("Open CSV"),
            on_click=open_file_picker,
        )
        return ft.Column(controls=[open_button, setup_text])

    csv_open_button = csv_loader(page)

    # Layout
    page.add(
        ft.Column(controls=[csv_open_button]),
        ft.Row(controls=[x_dropdown,y_dropdown], spacing=20, alignment="start"),
        ft.ElevatedButton("Train Model", on_click=train),
        input_field,
        ft.ElevatedButton("Predict", on_click=predict),
        result_text,
        coef_text,
        intercept_text,
        pred_text,
        image,
    )

### === Run App ===
ft.run(main)
