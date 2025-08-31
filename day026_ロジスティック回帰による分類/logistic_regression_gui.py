# logistic_regression_gui.py

### === Imports ===
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

import flet as ft
import matplotlib.pyplot as plt
import base64
import io
from dataclasses import dataclass
from typing import Optional

rng = np.random.default_rng(42)

### === Functions ===
@dataclass(slots=True)
class AppState:
    df: Optional[pd.DataFrame] = None
    model: Optional[LogisticRegression] = None
    X: Optional[np.ndarray] = None
    y: Optional[np.ndarray] = None

class Parameters:
    n_users = 1000
    lam_visits = 3.0
    beta0 = -2.0
    beta1 = 0.6

EMPTY_IMAGE = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgkL5Bp8AAAAASUVORK5CYII="
)

### === APP LOGICS ===
def main(page: ft.Page):
    page.title = "Logistic Regression Analysis"
    page.scroll = "auto"

    # UI Components
    result_text = ft.Text(value="Upload a CSV file to start.", size=16)
    coef_text = ft.Text("")
    intercept_text = ft.Text("")
    accuracy_text = ft.Text("")
    roc_auc_text = ft.Text("")
    confusion_matrix_text = ft.Text("")
    image = ft.Image(src_base64=EMPTY_IMAGE)
    probability_input = ft.TextField(label="Threshold(0-1)", width=200)

    # Params adjuster
    n_users_slider = ft.Slider(
        min=10, max=3000, divisions=99, value=100, label="{value}",
        on_change=lambda e: update_params()
    )
    beta1_field = ft.TextField(value="0.5", label="beta1", on_change=lambda e: update_params())

    params_text = ft.Text("Current settings: n_users=100, beta1=0.5")

    # Dropdowns for column selection
    x_dropdown = ft.Dropdown(label="Select feature (X)", options=[], width=250)
    y_dropdown = ft.Dropdown(label="Select target (y)", options=[], width=250)


    # 0) パラメータとState
    state = AppState()
    params = Parameters()

    ### Setup Functions
    def update_params():
        params.n_users = int(n_users_slider.value)
        params.beta1 = float(beta1_field.value)
        params_text.value = f"Current settings: n_users={params.n_users}, beta1={params.beta1}"
        page.update()

    def train_and_evaluate(df, threshold):
        try:
            # 学習・評価用のコード
            state.X = df[["visits"]].values
            state.y = df["purchased"].values
            X_train, X_test, y_train, y_test = train_test_split(
                state.X, state.y, test_size=0.25, random_state=42,stratify=state.y
            )
            clf = LogisticRegression(class_weight="balanced")
            clf.fit(X_train, y_train)

            proba = clf.predict_proba(X_test)[:, 1]
            pred = (proba >= threshold).astype(int)
            
            accuracy_text.value = f"Accuracy: {accuracy_score(y_test, pred)}"
            roc_auc_text.value = f"ROC-AUC: {roc_auc_score(y_test, proba)}"
            confusion_matrix_text.value = f"Confusion matrix:\n{confusion_matrix(y_test, pred)}"
            coef_text.value = f"coef: {clf.coef_}"
            intercept_text.value = f"intercept: {clf.intercept_}"
            result_text.value = "--- Calculation Result ---"
            # Show image
            fig, ax = plt.subplots()
            ax.scatter(X_test, y_test, color="blue", label="True labels")
            ax.scatter(X_test, proba, color="red", alpha=0.5, label="Predicted prob")
            ax.set_xlabel("Visits")
            ax.set_ylabel("Purchase probability")
            ax.legend()
            update_plot(fig, image)
            page.update()
        except Exception as err:
            result_text.value = f"Error occured: {err}"
            page.update()

    def update_plot(fig, image):
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        image.src_base64 = base64.b64encode(buf.read()).decode("utf-8")

    def csv_loader(page: ft.Page):
        setup_text = ft.Text()
        file_picker = ft.FilePicker()
        page.services.append(file_picker)
        async def open_file_picker(e: ft.Event[ft.ElevatedButton]):
            files = await file_picker.pick_files(allow_multiple=False)
            try:
                f = files[0]
            except Exception:
                setup_text.value = "Canceled to load CSV."
            try:
                df = pd.read_csv(f.path)
                state.df = df
                setup_text.value = f"CSV Loaded: {f.name} ({len(df)}items.)"

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
    open_csv_button = csv_loader(page)

    ### Main Analysis Functions
    def calculate_visits(e):
        try:
            threshold = float(probability_input.value)
        except ValueError:
            result_text.value = "Please enter a valid number (0-1)"
            page.update()
            return

        if state.df is None:
            result_text.value = "Please load CSV first (or simulate data)."
            page.update()
            return

        train_and_evaluate(state.df, threshold)
        """
        try:
            # 学習・評価用のコード
            state.X = state.df[["visits"]].values
            state.y = state.df["purchased"].values
            X_train, X_test, y_train, y_test = train_test_split(
                state.X, state.y, test_size=0.25, random_state=42,stratify=state.y
            )
            clf = LogisticRegression(class_weight="balanced")
            clf.fit(X_train, y_train)
            proba = clf.predict_proba(X_test)[:, 1]
            pred = (threshold >= proba).astype(int)
            
            accuracy_text.value = f"Accuracy: {accuracy_score(y_test, pred)}"
            roc_auc_text.value = f"ROC-AUC: {roc_auc_score(y_test, proba)}"
            confusion_matrix_text.value = f"Confusion matrix:\n{confusion_matrix(y_test, pred)}"
            coef_text.value = f"coef: {clf.coef_}"
            intercept_text.value = f"intercept: {clf.intercept_}"
            result_text.value = "--- Calculation Result ---"
            # Show image
            fig, ax = plt.subplots()
            ax.scatter(X_test, y_test, color="blue", label="True labels")
            ax.scatter(X_test, proba, color="red", alpha=0.5, label="Predicted prob")
            ax.set_xlabel("Visits")
            ax.set_ylabel("Purchase probability")
            ax.legend()
            update_plot(fig, image)
            page.update()
        except Exception as err:
            result_text.value = f"Error occured: {err}"
            page.update()"""

    def simulate_data(e):
        try:
            threshold = float(probability_input.value)
        except ValueError:
            result_text.value = "Please enter a valid number (0-1)"
            page.update()
            return
        # 1) 訪問回数（非負の整数）。ポアソンで左によった分布が作れる
        visits = rng.poisson(lam=params.lam_visits, size=params.n_users)
        # 2) ロジスティックで購入確率を計算
        logit = params.beta0 + params.beta1 * visits
        p = 1 / (1 + np.exp(-logit))
        # 3) 確率pで購入(1) / 非購入 (0)をサンプリング
        purchased = rng.binomial(1, p)

        df = pd.DataFrame({
            "user_id": np.arange(1, params.n_users + 1),
            "visits": visits,
            "purchased": purchased
            })
        df.to_csv("Simulated_visits_purchase.csv", index=False)
        #print(df.head())
        #print("Positives rate:", df["purchased"].mean())

        train_and_evaluate(df, threshold)
        """try:
            # 学習・評価用のコード
            state.X = df[["visits"]].values
            state.y = df["purchased"].values
            X_train, X_test, y_train, y_test = train_test_split(
                state.X, state.y, test_size=0.25, random_state=42,stratify=state.y
            )
            clf = LogisticRegression(class_weight="balanced")
            clf.fit(X_train, y_train)

            proba = clf.predict_proba(X_test)[:, 1]
            pred = (proba >= threshold).astype(int)
            
            accuracy_text.value = f"Accuracy: {accuracy_score(y_test, pred)}"
            roc_auc_text.value = f"ROC-AUC: {roc_auc_score(y_test, proba)}"
            confusion_matrix_text.value = f"Confusion matrix:\n{confusion_matrix(y_test, pred)}"
            coef_text.value = f"coef: {clf.coef_}"
            intercept_text.value = f"intercept: {clf.intercept_}"
            result_text.value = "--- Calculation Result ---"
            # Show image
            fig, ax = plt.subplots()
            ax.scatter(X_test, y_test, color="blue", label="True labels")
            ax.scatter(X_test, proba, color="red", alpha=0.5, label="Predicted prob")
            ax.set_xlabel("Visits")
            ax.set_ylabel("Purchase probability")
            ax.legend()
            update_plot(fig, image)
            page.update()
        except Exception as err:
            result_text.value = f"Error occured: {err}"
            page.update()"""




    ### Layout
    page.add(
        ft.Column(controls=[open_csv_button]),
        ft.ElevatedButton("Calculate", on_click=calculate_visits),
        result_text,
        accuracy_text,
        roc_auc_text,
        confusion_matrix_text,
        coef_text,
        intercept_text,
        image,
        ft.Divider(),
        probability_input,
        n_users_slider,
        beta1_field,
        params_text,
        ft.ElevatedButton("Simulate Data", on_click=simulate_data)
    )

### === Run App ===
ft.run(main)
