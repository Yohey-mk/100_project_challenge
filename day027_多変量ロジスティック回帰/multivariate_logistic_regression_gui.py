# multivariate_logistic_regression_gui.py

### === Imports ===
import io
import base64
from dataclasses import dataclass
from typing import Optional, List

import flet as ft
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

# === RNG ===
rng = np.random.default_rng(42)

# === dataclasses ===
@dataclass(slots=True)
class AppState:
    df: Optional[pd.DataFrame] = None
    model: Optional[LogisticRegression] = None
    X: Optional[np.ndarray] = None
    y: Optional[np.ndarray] = None
    feature_names: Optional[List[str]] = None

@dataclass(slots=True)
class Parameters:
    # Generate data
    n_users: int = 1000
    lam_visits: float = 5.0
    beta0: float = -2.0
    beta1: float = 0.15 # visitsの効果
    beta2: float = 1.0 # is_memberの効果
    beta3: float = 1.2 # is_repeatの効果
    beta4: float = 1.5 # price_sensitivityの負の効果（下で-beta4として加わる）
    # 推論時の閾値
    threshold: float = 0.5

EMPTY_IMAGE = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgkL5Bp8AAAAASUVORK5CYII="
)

# === helper: matplotlib -> base64 ===
def fig_to_base64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    #fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    #plt.close(fig)
    buf.seek(0)
    img_base_64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base_64

# === data simulation ===
def simulate_df(params: Parameters) -> pd.DataFrame:
    n = params.n_users
    visits = rng.poisson(lam=params.lam_visits, size=n)

    # generate member/repeater
    p_member = 1 / (1 + np.exp(-(-2 + 0.4 * visits))) # 低訪問では低く、多訪問で高く
    is_member = rng.binomial(1, p_member)

    p_repeat = 1 / (1 + np.exp(-(-3 + 0.5 * visits))) # こちらもVisitsに依存
    is_repeat = rng.binomial(1, p_repeat)

    price_sensitivity = rng.random(n) # 0~1 一様

    # 多変量ロジスティックの真の生成式
    logit = (
        params.beta0
        + params.beta1 * visits
        + params.beta2 * is_member
        + params.beta3 * is_repeat
        - params.beta4 * price_sensitivity
    )
    p = 1 / (1 + np.exp(-logit))
    purchased = rng.binomial(1, p)

    df = pd.DataFrame(
        {
            "user_id": np.arange(1, n + 1),
            "visits": visits,
            "is_member": is_member,
            "is_repeat": is_repeat,
            "price_sensitivity": price_sensitivity,
            "purchased": purchased,
        }
    )
    return df

# === training and evaluation ===
REQUIRED_COLS = ["visits", "is_member", "is_repeat", "price_sensitivity", "purchased"]
FEATURES = ["visits", "is_member", "is_repeat", "price_sensitivity"]

def train_and_evaluate(state: AppState, df: pd.DataFrame, threshold: float):
    for c in REQUIRED_COLS:
        if c not in df.columns:
            raise ValueError(f"CSVに必要な列がありません: {c}")
        
    X = df[FEATURES].values
    y = df["purchased"].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(X_train, y_train)

    proba = clf.predict_proba(X_test)[:, 1]
    pred = (proba >= threshold).astype(int)

    metrics = {
        "accuracy": accuracy_score(y_test, pred),
        "roc_auc": roc_auc_score(y_test, proba),
        "cm": confusion_matrix(y_test, pred),
        "coef": clf.coef_[0], # shape: (4,)
        "intercept": clf.intercept_[0],
    }

    state.df = df
    state.X = X
    state.y = y
    state.model = clf
    state.feature_names = FEATURES

    # 可視化: visits vs (true/pred-proba)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(X_test[:, 0], y_test, alpha=0.4, label="True label (0/1)")
    ax.scatter(X_test[:, 0], proba, alpha=0.5, label="Predicted probability")

    # visitsの各ユニーク値で平均確率を選で表示
    uniq = np.unique(X_test[:, 0])
    mean_prob = [proba[X_test[:, 0] == u].mean() for u in uniq]
    ax.plot(uniq, mean_prob, linewidth=2, label="Mean predicted prob by visits")

    ax.set_xlabel("visits")
    ax.set_ylabel("probability / label")
    ax.set_title("Visits vs Probability / Label")
    ax.legend()

    img_b64 = fig_to_base64(fig)

    return metrics, img_b64

# === Help texts ===
HELP_TEXT = {
    "threshold": (
        "閾値(Threshold)\n"
        "予測確率がこの値以上なら 1(=購入) と判定し、それ未満は 0(=非購入) とします。\n"
        "例: 0.5 を選べば、50% 以上の確率を『購入』とみなします。"
    ),
    "beta": (
        "Beta(係数)の意味\n"
        "ロジスティック回帰の線形予測子: logit(p)=b0 + b1*visits + b2*is_member + b3*is_repeat + b4*price...\n"
        "係数が正なら、その特徴量が増えると『購入のオッズ』が上がる(=購入しやすくなる)ことを意味します。\n"
        "係数の指数 exp(beta) は『オッズ比』で、1単位増でオッズが何倍になるかを表します。"
    ),
    "beta0_detail": (
        """
        •	beta0 (intercept)
        •	全ての特徴量がゼロのときの「基準の購入しやすさ」。
        •	値を大きくすると、全体的に購入確率が底上げされる。小さくすると全体的に購入が起きにくくなる。
        •	意味: 市場全体の購入しやすさの基準を設定。
        """
    ),
    "beta1_detail": (
        """
        •	beta1 (visits)
        •	訪問回数が1回増えるごとに、購入オッズがどのくらい増えるか。
	    •	値を大きくすると「たくさん訪問する人は買いやすい」という関係が強まる。
	    •	小さくすると「訪問回数と購入の関係は弱い」という設定になる。
	    •	意味: 「リピーターは買いやすい」効果の強さ。
        """
    ),
    "beta2_detail": (
        """
        •	beta2 (is_member)
        •	会員かどうかで購入オッズがどのくらい上がるか。
	    •	値を大きくすると「会員は非会員より買いやすい」という差が大きくなる。
	    •	値をゼロにすると、会員と非会員の差はなくなる。
	    •	意味: 会員制度がどれだけ購買行動に影響するか。
        """
    ),
    "beta3_detail": (
        """
        •	beta3 (is_repeat)
	    •	過去に購入した人（リピーター）が再購入する確率の高さ。
	    •	値を大きくすると「一度買った人はまた買う」効果が強調される。
	    •	意味: ロイヤリティ（リピーター効果）の強さ。
        """
    ),
    "beta4_detail": (
        """
        •	beta4 (price_sensitivity)
	    •	価格に敏感なユーザーほど購入しにくい効果。
	    •	値を大きくすると「価格に敏感な人はさらに買わない」設定になる。
	    •	値を小さくすると「価格敏感度の影響が弱まる」。
	    •	意味: 値引きや価格設定が購買にどのくらい影響するか。
        """
    ),
    "metrics": (
        "主要な評価指標\n"
        "• Accuracy: 全予測のうち正解した割合。クラス不均衡に弱い可能性があります。\n"
        "• ROC-AUC: 0〜1。大きいほど判別能力が高い。閾値に依存しません。\n"
        "• Confusion Matrix: 予測/真値のクロス表 (TN, FP, FN, TP)。"
    ),
}

# === Flet App ===
def main(page: ft.Page):
    page.title = "Multivariable Logistic Regression"
    page.scroll = "auto"
    page.window.width = 1200
    page.window.height = 800

    state = AppState()
    params = Parameters()

    # UI Components
    # pics
    img_view = ft.Image(src_base64=EMPTY_IMAGE, width=640, height=400, fit=ft.BoxFit.CONTAIN)

    # Result texts
    acc_text = ft.Text("")
    auc_text = ft.Text("")
    cm_text = ft.Text("")

    # 係数テーブル用placeholder
    coef_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Feature")),
            ft.DataColumn(ft.Text("Coefficient")),
            ft.DataColumn(ft.Text("Odds Ratio (exp)")),
        ],
        rows=[]
    )

    # === Controls: Threshold and Info ===
    threshold_field = ft.TextField(label="Threshold (0-1)", value=str(params.threshold), width=220)
    threshold_help = ft.ExpansionTile(title=ft.Text("❓️Thresholdの説明"),
                                      controls=[ft.Text(HELP_TEXT["threshold"])])
    
    # === Explanations (Expansion tile/markdown) ===
    metrics_help = ft.ExpansionTile(title=ft.Text("❓️Metricsの説明"),
                                    controls=[ft.Text(HELP_TEXT["metrics"])])
    explain_md = ft.Markdown(
        """
### 用語の説明
- **Threshold**: 予測確率がこの値以上なら 1(購入) と判定。それ未満は 0(非購入)。
- **Accuracy**: (TP+TN)/(全件)。クラス不均衡では過大評価に注意。
- **ROC-AUC**: 0.5=ランダム, 1.0=完全。閾値に依存せずモデルの識別力を測る。
- **Confusion Matrix**: 予測と真値のクロス表。[[TN, FP],[FN, TP]]。
- **Beta (係数)**: 1単位増でオッズが exp(beta) 倍。符号が正なら購入しやすく、負なら購入しにくい。
    """,
    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
    selectable=True,
    )

    beta_help = ft.ExpansionTile(title=ft.Text("❓️Betaの説明"),
                                 controls=[ft.Text(HELP_TEXT["beta"])], initially_expanded=False)
    beta0_help = ft.ExpansionTile(title=ft.Text("❓️Beta0の説明"),
                                  controls=[ft.Text(HELP_TEXT["beta0_detail"])], initially_expanded=False)
    beta1_help = ft.ExpansionTile(title=ft.Text("❓️Beta1の説明"), 
                                  controls=[ft.Text(HELP_TEXT["beta1_detail"])], initially_expanded=False)
    beta2_help = ft.ExpansionTile(title=ft.Text("❓️Beta2の説明"),
                                  controls=[ft.Text(HELP_TEXT["beta2_detail"])], initially_expanded=False)
    beta3_help = ft.ExpansionTile(title=ft.Text("❓️Beta3の説明"),
                                  controls=[ft.Text(HELP_TEXT["beta3_detail"])], initially_expanded=False)
    beta4_help = ft.ExpansionTile(title=ft.Text("❓️Beta4の説明"),
                                  controls=[ft.Text(HELP_TEXT["beta4_detail"])], initially_expanded=False)
    beta_details = ft.ExpansionTile(title=ft.Text("❓️Beta0 - 4の詳細"),
        controls=[ft.Column([beta0_help,
                              beta1_help,
                              beta2_help,
                              beta3_help,
                              beta4_help])], initially_expanded=False)

    # === Controls: simulation params ===
    n_users_slider = ft.Slider(min=100, max=10000, divisions=99, value=params.n_users, label="{value}")
    lam_slider = ft.Slider(min=0.5, max=10.0, divisions=95, value=params.lam_visits, label="{value}")

    beta0_field = ft.TextField(label="beta0 (intercept)", value=str(params.beta0), width=180)
    beta1_field = ft.TextField(label="beta1 (visits)", value=str(params.beta1), width=180)
    beta2_field = ft.TextField(label="beta2 (is_member)", value=str(params.beta2), width=180)
    beta3_field = ft.TextField(label="beta3 (is_repeat)", value=str(params.beta3), width=180)
    beta4_field = ft.TextField(label="beta4 (price_sensitivity; 負の効果)", value=str(params.beta4), width=260)

    # === Dropdowns ===
    x_dropdown = ft.Dropdown(label="Select feature (X)", options=[], width=250)
    y_dropdown = ft.Dropdown(label="Select target (y)", options=[], width=250)

    # Read files
    file_info = ft.Text("")

    def read_csv(page: ft.Page):
        setup_text = ft.Text()
        file_picker = ft.FilePicker()
        page.services.append(file_picker)
        async def open_file_picker(e: ft.Event[ft.ElevatedButton]):
            files = await file_picker.pick_files(allow_multiple=False)
            try:
                f = files[0]
            except Exception:
                setup_text.value = "Canceled to load csv."
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
            content=ft.Text("OPEN CSV"),
            on_click=open_file_picker,
        )
        return ft.Column(controls=[open_button, setup_text])
    open_csv_button = read_csv(page)

    # === actions ===
    def parse_params_from_ui() -> Optional[str]:
        try:
            params.n_users = int(n_users_slider.value)
            params.lam_visits = float(lam_slider.value)
            params.beta0 = float(beta0_field.value)
            params.beta1 = float(beta1_field.value)
            params.beta2 = float(beta2_field.value)
            params.beta3 = float(beta3_field.value)
            params.beta4 = float(beta4_field.value)
            params.threshold = float(threshold_field.value)
            if not (0.0 <= params.threshold <= 1.0):
                return "Thresholdは0~1の数値で指定してください"
        except Exception as err:
            return f"パラメータの数値化に失敗しました：{err}"
        return None
    
    def refresh_coef_table(coef: np.ndarray, feature_names: List[str]):
        rows = []
        for name, c in zip(feature_names, coef):
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(name)),
                    ft.DataCell(ft.Text(f"{c:.4f}")),
                    ft.DataCell(ft.Text(f"{np.exp(c):.4f}")),
                ])
            )
        coef_table.rows = rows

    def run_training(df: pd.DataFrame):
        try:
            metrics, img_b64 = train_and_evaluate(state, df, params.threshold)
            acc_text.value = f"Accuracy: {metrics['accuracy']:.4f}"
            auc_text.value = f"ROC-AUC: {metrics['roc_auc']:.4f}"
            cm = metrics["cm"]
            cm_text.value = (
                "Confusion Matrix\n"
                f"[[TN={cm[0,0]} FP={cm[0,1]}]\n [FN={cm[1,0]} TP={cm[1,1]}]]"
            )

            refresh_coef_table(metrics["coef"], state.feature_names)
            img_view.src_base64 = img_b64
            page.update()
        except Exception as err:
            acc_text.value = f"Error: {err}"
            auc_text.value = ""
            cm_text.value = ""
            page.update()

    def on_simulate_click(e):
        msg = parse_params_from_ui()
        if msg:
            acc_text.value = msg
            auc_text.value = ""
            cm_text.value = ""
            page.update()
            return
        df = simulate_df(params)
        state.df = df
        file_info.value = f"Simulated: {len(df)} rows (positives={df['purchased'].mean():.3f})"
        run_training(df)

    def on_train_click(e):
        msg = parse_params_from_ui()
        if msg:
            acc_text.value = msg
            auc_text.value = ""
            cm_text.value = ""
            page.update()
            return
        if state.df is None:
            acc_text.value = "先にCSVを読み込むかSimulateしてください"
            auc_text.value = ""
            cm_text.value = ""
            page.update()
            return
        run_training(state.df)

    # === Layout ===
    # left: read data/simulation
    left_card = ft.Card(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("1) Data", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([open_csv_button, file_info], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Text("Simulation Settings", weight=ft.FontWeight.BOLD),
                    ft.Column([ft.Text("n_users"), n_users_slider]),
                    ft.Column([ft.Text("lam_visits"), lam_slider]),
                    ft.Column([beta_help, ft.Text("Beta(係数)")]),
                    ft.Row([
                        ft.Container(beta0_field, padding=0),
                        ft.Container(beta1_field, padding=0)]),
                    ft.Row([
                        ft.Container(beta2_field, padding=0),
                        ft.Container(beta3_field, padding=0)]),
                    ft.Container(beta4_field, padding=0),
                    ft.Column([ft.Text("💡 Beta パラメータの意味とスライダ調整の意図"),
                               beta_details]),
                    ft.Column([threshold_help, threshold_field]),
                    ft.Row([
                        ft.ElevatedButton("Simulate + Train", on_click=on_simulate_click),
                        ft.ElevatedButton("Train/Evaluate (CSV)", on_click=on_train_click),
                    ]),
                ],
                tight=True,
                spacing=8,
            ),
            padding=8,
            width=430,
        )
    )

    # right: Result and visualize
    right_card = ft.Card(
        ft.Container(
            content=ft.Column([
                ft.Text("2) 評価", size=18, weight=ft.FontWeight.BOLD),
                ft.Column([metrics_help, ft.Text("Metrics")]),
                acc_text,
                auc_text,
                cm_text,
                ft.Text("係数とオッズ比"),
                coef_table,
                ft.Text("Visualize: Visits vs Probability/Label"),
                img_view,
                ft.Divider(),
                explain_md,
            ]),
            padding=12,
            expand=True,
        )
    )

    page.add(
        ft.Row(
            controls=[left_card, right_card],
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.START,
        )
    )

### === RUN APP ===
ft.run(main)