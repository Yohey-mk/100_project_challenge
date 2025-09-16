# k_nn_cui.py

### === Imports ===
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder

### === sample data creation ===
items = []
sex_options = ["Men", "Women", "Kids", "Unknown"]
age_options = ["10s", "20s", "30s", "40s", "50s", "60s+"]
shoe_types = ["sneaker", "boot", "sandal", "running", "basket", "golf"]
colors = ["black", "white", "gray", "blue", "red", "brown", "other"]

rng = np.random.default_rng(123)

for item_id in range(1, 101):
    sex = rng.choice(sex_options, p=[0.4, 0.4, 0.1, 0.1])
    age = rng.choice(age_options, p=[0.05, 0.25, 0.3, 0.2, 0.15, 0.05])
    t = rng.choice(shoe_types)
    c = rng.choice(colors)
    items.append({"item_id": item_id, "sex": sex, "age": age, "type": t, "color": c})

items_df = pd.DataFrame(items)

### === One-Hot Encoding(カテゴリ特徴) ===
enc = OneHotEncoder(sparse_output=False)
X = enc.fit_transform(items_df[["sex", "age", "type", "color"]])

### === NearestNeighborsを作ってアイテムの近傍を事前計算 ===
nn = NearestNeighbors(n_neighbors=6, metric="cosine").fit(X) # 自分自身を含めて6, 1は自分
distances, indices = nn.kneighbors(X)

### === Helper: 推薦関数(user_purchased: list of item_id)
def recommend_for_user(user_purchased, top_k=5):
    # 集計スコア:近傍で見つかった頻度 / 類似度を足し合わせる
    score = {}
    for item_id in user_purchased:
        idx = items_df.index[items_df["item_id"] == item_id][0]
        neigh_idxs = indices[idx][1:] # 0が自分なので除外
        neigh_dists = distances[idx][1:]
        for ni, d in zip(neigh_idxs, neigh_dists):
            iid = int(items_df.loc[ni, "item_id"])
            if iid in user_purchased:
                continue
            # 類似度として（1 - cosince_distance）
            sim = 1 - d
            score[iid] = score.get(iid, 0.0) + sim

    # 上位top_kを返す
    ranked = sorted(score.items(), key=lambda x: x[1], reverse=True)
    return [iid for iid, s in ranked[:top_k]]

### === Test: 仮ユーザーがitem 5と20を購入していたケース ===
user_purchased = [5, 20]
print("User purchased:", user_purchased)
print("Recommend:", recommend_for_user(user_purchased, top_k=5))