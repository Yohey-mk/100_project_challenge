# decision_tree_and_random_forest.py

from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Titanic dataを取得
df = fetch_openml("titanic", version=1, as_frame=True).frame

# "survived"を目的変数にする
y = df["survived"]
X = df.drop("survived", axis=1)

# Category -> one-hot
X = pd.get_dummies(X, drop_first=True)

# 欠損値は中央値で埋める（RandomForestはこれでOK）
X = X.fillna(X.median())

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 決定木で分類
tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_train, y_train)

y_pred_tree = tree.predict(X_test)
acc_tree = accuracy_score(y_test, y_pred_tree)
print("Decision Tree Accuracy: ", acc_tree)

# ランダムフォレストで分類
forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
forest.fit(X_train, y_train)

y_pred_forest = forest.predict(X_test)
acc_forest = accuracy_score(y_test, y_pred_forest)
print("Random Forest Accuracy:", acc_forest)

# 重要な特徴量を可視化
importances = forest.feature_importances_
indices = np.argsort(importances[::-1])

plt.figure(figsize=(10, 6))
plt.bar(range(10), importances[indices][:10])
plt.xticks(range(10), X.columns[indices][:10], rotation=45)
plt.title("Top 10 Important Features")
plt.tight_layout()
plt.show()

# 決定木の深さと精度の関係 *これをmatplotlibで折れ線グラフで可視化する。⭐️ToDo
depths = range(1, 20)
scores = []

for d in depths:
    model = DecisionTreeClassifier(max_depth=d, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    scores.append(accuracy_score(y_test, pred))

plt.figure(figsize=(8, 5))
plt.plot(depths, scores, marker="o")
plt.xlabel("Depth of Decision Tree")
plt.ylabel("Accuracy")
plt.title("Decision Tree: Depth vs Accuracy")
plt.grid(True)
plt.tight_layout()
plt.show()

# Notes
#🧠 学べること
#	•	機械学習の基本ワークフロー（前処理→学習→評価）
#	•	決定木の「木構造」の意味
#	•	ランダムフォレストの仕組み（複数の木で投票）
#	•	テーブルデータの扱い方
#	•	特徴量の重要度の見方
#🧠 追加の学びポイント（できれば後でやってみて）
#✔ 1. train accuracy も同時に描くと過学習が見える
#深い木ほど「訓練精度100%」になるので、強烈にわかりやすい。
#✔ 2. ランダムフォレストの n_estimators を変えて同じグラフを作る
#こちらも深い理解に役立ちます。