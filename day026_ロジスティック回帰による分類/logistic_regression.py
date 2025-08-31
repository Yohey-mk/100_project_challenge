# logistic_regression.py

### Imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

rng = np.random.default_rng(42)

# パラメータ（自分で色んな数値を入力し、理解を深める）
n_users = 1000
lam_visits = 3.0
beta0 = -2.0
beta1 = 0.6

# 1) 訪問回数（非負の整数）。ポアソンで左によった分布が作れる
visits = rng.poisson(lam=lam_visits, size=n_users)

# 2) ロジスティックで購入確率を計算
logit = beta0 + beta1 * visits
p = 1 / (1 + np.exp(-logit))

# 3) 確率pで購入(1) / 非購入 (0)をサンプリング
purchased = rng.binomial(1, p)

df = pd.DataFrame({
    "user_id": np.arange(1, n_users + 1),
    "visits": visits,
    "purchased": purchased
})

df.to_csv("visits_purchase.csv", index=False)
print(df.head())
print("Positives rate:", df['purchased'].mean())

# 学習・評価用のコード
df = pd.read_csv("visits_purchase.csv")
X = df[["visits"]].values
y = df["purchased"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 不均衡になりがちなのでbalancedをつけると学びやすい
clf = LogisticRegression(class_weight="balanced")
clf.fit(X_train, y_train)

proba = clf.predict_proba(X_test)[:, 1]
pred = (proba >= 0.5).astype(int)

print("Accuracy:", accuracy_score(y_test, pred))
print("ROC-AUC:", roc_auc_score(y_test, proba))
print("Confusion matrix;\n", confusion_matrix(y_test, pred))
print("coef, intercept:", clf.coef_, clf.intercept_)