# day042_knn_simulator.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier


st.set_page_config(page_title="k-NN Simulator", layout="wide")
st.title("🤖 目で見て分かる！k-NN（k近傍法）シミュレーター")

# 1. データの生成（キャッシュして毎回データが変わるのを防ぐ）
@st.cache_data
def load_data():
    # 2次元（特徴量が２つ）で、２つのクラスに分かれるダミーデータ作成
    X, y = make_classification(
        n_samples=200,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        random_state=42,
        class_sep=1.2 # データ同士の離れ具合
    )
    return X, y

X, y = load_data()

# UIとグラフ

# 2. サイドバーにｋの値を決めるスライダーを設置
k = st.sidebar.slider("kの値を1〜20から設定してください", min_value=1, max_value=20)

# 3. K-NNモデルの定義と学習
model = KNeighborsClassifier(n_neighbors=k)
model.fit(X, y)

# 現在のモデルが手元のデータ（X, y）をどれくらい正確に分類できているか正解率を計算
accuracy = model.score(X, y)
st.sidebar.metric("正解率(Accuracy)", f"{accuracy * 100:.1f}%")

# 4. グラフの描画（まずは単純な散布図を作ってみる）
# --- 1. 背景を塗るための「方眼紙」を用意する
# X軸とY軸の最小値、最大値を求め、グラフの端まで色が塗られるように少し余白をもたせる（+-1）
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

# 0.05刻みで細かい網目を作成（方眼紙の交点）
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.05),
                     np.arange(y_min, y_max, 0.05))

# --- 2. 方眼紙のすべての点でAIに予測させる
# xx.ravel()で配列を１列に伸ばし、np.c_でX座標とY座標のペアにする
grid_points = np.c_[xx.ravel(), yy.ravel()]
Z = model.predict(grid_points)

# 予測結果を元の方眼紙の形に戻す
Z = Z.reshape(xx.shape)

# --- 3. Matplotlibでグラフを描く
fig, ax = plt.subplots(figsize=(10, 6))

# 背景を予測結果（Z）に基づいて塗りつぶす(cmap="coolwarm")で青と赤にする
ax.contourf(xx, yy, Z, alpha=0.3, cmap="coolwarm")

# 実際のデータ点（X）を散布図として上から重ねる
# c=yでクラスごとに色を分け、edgecolor='k'で点に黒い縁をつける
ax.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap='coolwarm', s=50)

ax.set_title(f"k-NN Decision Boundary (k = {k})")
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")

# Streamlitの画面に表示
st.pyplot(fig)