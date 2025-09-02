# multivariate_logistic_regression_cui.py

### === Imports ===
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
from dataclasses import dataclass
from typing import Optional

rng = np.random.default_rng(42)

# Parameters
@dataclass(slots=True)
class Parameters:
    n_users = 1000
    lam_visits = 5.0
    beta0 = -2.0
    beta1 = 0.15
    beta2 = 1.0 # repeaterは購入しやすい
    beta3 = 1.2 # is_memberは購入しやすい
    beta4 = 1.5 #価格敏感だと買いにくい

class AppState:
    model: Optional[LogisticRegression] = None
    df: Optional[pd.DataFrame] = None
    X: Optional[np.ndarray] = None
    y: Optional[np.ndarray] = None

params = Parameters()
state = AppState()

# 1) Visits, Is_member, Is_repeatの生成
visits = rng.poisson(lam=params.lam_visits, size=params.n_users)
p_member = 1 / (1 + np.exp(-( -2 + 0.4 * visits)))
is_member = rng.binomial(1, p_member)
p_repeat = 1 / (1 + np.exp(-( -3 + 0.5 * visits)))
is_repeat = rng.binomial(1, p_repeat)
price_sensitivity = np.random.rand(params.n_users)

# 2) 多変量ロジスティックで購入確率を計算
logit = (params.beta0
         + params.beta1 * visits
         + params.beta2 * is_member
         + params.beta3 * is_repeat
         - params.beta4 * price_sensitivity)
p = 1 / (1 + np.exp(-logit))

# 3) 確率pで購入(1) / 非購入(0)をサンプリング
purchased = rng.binomial(1, p)

df = pd.DataFrame({
    "user_id": np.arange(1, params.n_users + 1),
    "visits": visits,
    "is_member": is_member,
    "is_repeat": is_repeat,
    "price_sensitivity": price_sensitivity,
    "purchased": purchased
})

df.to_csv("multivariable_logistic_regression.csv", index=False)
print(df.head())
print("Positives rate:", df['purchased'].mean())
#print(state.model.coef_)

def train_and_evaluate(df):
    try:
        state.X = df[["visits", "is_member", "is_repeat", "price_sensitivity"]].values
        state.y = df["purchased"].values
        X_train, X_test, y_train, y_test = train_test_split(
            state.X, state.y, test_size=0.25, random_state=42, stratify=state.y
        )
        clf = LogisticRegression(class_weight="balanced")
        clf.fit(X_train, y_train)

        proba = clf.predict_proba(X_test)[:, 1]
        pred = (proba >= 0.5).astype(int)

        print("Accuracy:", accuracy_score(y_test, pred))
        print("ROC-AUC:", roc_auc_score(y_test, proba))
        print("Confusion matrix:\n", confusion_matrix(y_test, pred))
        print("coef, intercept:", clf.coef_, clf.intercept_)
    except Exception as err:
       result = f"Error occured: {err}"
       print(result)

train_and_evaluate(df)