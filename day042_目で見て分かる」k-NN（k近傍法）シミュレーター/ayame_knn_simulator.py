# ayame_knn_simulator.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

st.set_page_config(page_title="Iris k-NN Simulator", layout='wide')
st.title("🌸 アヤメ(Iris)の品種分類シミュレーター")
st.markdown("現実のデータを使って, 3種類のアヤメの境界線がどう引かれるか見てみましょう")

# 1. データの生成（キャッシュ）
@st.cache_data
def load_iris_data():
    # 1. Irisデータセットを読み込む
    iris = load_iris()

    # 2. 特徴量（データ本体=X）とターゲット（正解ラベル=y）を取得する
    # ※irisの中には.data(特徴量)と.target(正解ラベル)が入っているので、それを取得する
    X_full = iris.data
    y = iris.target

    # 全４つの特徴の内、２番め（花びらの長さ）と３番め（花びらの幅）の２列だけを抽出する
    X_2d = X_full[:, [2, 3]]

    return X_2d, y, iris.target_names, iris.feature_names

X, y, target_names, feature_names = load_iris_data()

# 2. サイドバーにkの値を決めるスライダーを設置
k = st.sidebar.slider("kの値を1~20から設定してください", min_value=1, max_value=20)

# 3. K-NNモデルの定義と学習
model = KNeighborsClassifier(n_neighbors=k)
model.fit(X, y)

# 正解率の計算と表示
accuracy = model.score(X, y)
st.sidebar.metric("正解率(Accuracy)", f"{accuracy * 100:.1f}%")

# 4. グラフの描画（決定境界と散布図）
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5

# 網目（方眼紙）を作成
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                     np.arange(y_min, y_max, 0.02))

# 予測
grid_points = np.c_[xx.ravel(), yy.ravel()]
Z = model.predict(grid_points)
Z = Z.reshape(xx.shape)

fig, ax = plt.subplots(figsize=(10, 6))

# カラーリング（３色）
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF']) # background
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF']) # dots

# 背景を塗りつぶす
ax.contourf(xx, yy, Z, alpha=0.3, cmap=cmap_light)

# 実際のデータ点（X）を散布図として上から重ねる
scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolors='k', s=50)

# 凡例（花の名前）を追加
handles, _ = scatter.legend_elements()
ax.legend(handles, target_names, title="Type of Iris")

ax.set_title(f"Iris 3-Class Classification (k = {k})")
ax.set_xlabel(feature_names[2]) # 花弁の長さ
ax.set_ylabel(feature_names[3]) # 花びらの幅

# Streamlitの画面に表示
st.pyplot(fig)