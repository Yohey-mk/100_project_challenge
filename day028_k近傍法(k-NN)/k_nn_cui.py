# k_nn_cui.py

### === Imports ===
import numpy as np
import pandas as pd
import random
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder

from train_test_split import get_dfs, train_test_split_by_user, UserBasedRecommender, precision_at_k, mean_precision_at_k

### === sample data creation ===
# ---Not in use from here *Sampleデータをランダム生成するために使用した。備忘録として残している。
#items = []
#sex_options = ["Men", "Women", "Kids", "Unknown"]
#age_options = ["10s", "20s", "30s", "40s", "50s", "60s+"]
#shoe_types = ["sneaker", "boot", "sandal", "running", "basket", "golf"]
#colors = ["black", "white", "gray", "blue", "red", "brown", "other"]
#
#rng = np.random.default_rng(123)
#
# item master
#item_master = []
#n_items = 100
#for item_id in range(1, n_items+1):
#    sex = rng.choice(sex_options, p=[0.4, 0.4, 0.1, 0.1])
#    age = rng.choice(age_options, p=[0.05, 0.25, 0.3, 0.2, 0.15, 0.05])
#    t = rng.choice(shoe_types)
#    c = rng.choice(colors)
#    item_master.append({"item_id": item_id, "sex": sex, "age": age, "type": t, "color": c})
#
#item_master_df = pd.DataFrame(item_master)
#
# user purchase history
#items = []
#for user_id in range(1, 3001):
#    purchased = random.sample(range(1, n_items+1), k=5)
#    for item_id in purchased:
#        item = item_master_df[item_master_df["item_id"] == item_id].iloc[0].to_dict()
#        record = {"user_id": user_id, **item}
#        items.append(record)
#        
# DataFrame & CSV化
#items_df = pd.DataFrame(items)
#items_df.to_csv("user_purchses.csv", index=False)
# ---to here

### === Read CSV (*After generated a csv from above) ===
items_df = get_dfs()
item_master_df = items_df.drop_duplicates("item_id")[["item_id", "sex", "age", "type", "color"]].reset_index(drop=True)

train_df, test_df = train_test_split_by_user(items_df, test_size=0.2)
recommender = UserBasedRecommender(train_df, item_master_df, n_neighbors=6)
user_id = 35
print(f"Recommend for user {user_id}:")
print(recommender.recommend(user_id=user_id, top_k=5, with_attributes=True))
mean_p5 = mean_precision_at_k(recommender, test_df, k=5, max_users=200)
print("Mean Precision@5:", mean_p5)
print("---------\n")

### === One-Hot Encoding(カテゴリ特徴) ===
enc = OneHotEncoder(sparse_output=False)
X = enc.fit_transform(item_master_df[["sex", "age", "item_id", "type", "color"]])

### === NearestNeighborsを作ってアイテムの近傍を事前計算 ===
nn = NearestNeighbors(n_neighbors=6, metric="cosine").fit(X) # 自分自身を含めて6, 1は自分
distances, indices = nn.kneighbors(X)

### === Helper: 推薦関数(user_purchased: list of item_id)
### =-=-= Item-Based Recommendation =-=-= ###
def recommend_for_user(user_purchased, top_k=10):
    # 集計スコア:近傍で見つかった頻度 / 類似度を足し合わせる
    score = {}
    for item_id in user_purchased:
        idx = item_master_df.index[item_master_df["item_id"] == item_id][0]
        neigh_idxs = indices[idx][1:] # 0が自分なので除外
        neigh_dists = distances[idx][1:]
        for ni, d in zip(neigh_idxs, neigh_dists):
            iid = int(item_master_df.loc[ni, "item_id"])
            if iid in user_purchased:
                continue
            # 類似度として（1 - cosince_distance）
            sim = 1 - d
            score[iid] = score.get(iid, 0.0) + sim

    # 上位top_kを返す
    ranked = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top_items = [iid for iid, _ in ranked[:top_k]]
    # item_idではなく属性を返す
    results = item_master_df[item_master_df["item_id"].isin(top_items)][["item_id", "sex", "age", "type", "color"]]
    return results

### === Test: 仮ユーザーがitem 5と20を購入していたケース ===
user_purchased = [5, 20]
print("User purchased:", user_purchased)
print("Recommend:\n", recommend_for_user(user_purchased, top_k=10))

### =-=-= User-Based Recommendation =-=-= ###
### === User-Item行列を作成 ===
user_item_matrix = pd.crosstab(items_df["user_id"], items_df["item_id"])

# NearestNeiborsをユーザー行列に適用
nn_user = NearestNeighbors(n_neighbors=6, metric="cosine").fit(user_item_matrix)
distances_u, indices_u = nn_user.kneighbors(user_item_matrix)

### === Helper: ユーザーベース推薦 === ***Topのrecommenderで代替するので以下不要
def recommend_for_user_based(user_id, top_k=5):
    #対象ユーザーの行番号
    idx = user_item_matrix.index.get_loc(user_id)

    #近いユーザー（自分を除く）
    neigh_idxs = indices_u[idx][1:]
    neigh_dists = distances_u[idx][1:]

    #すでに対象ユーザが購入したものは除外する
    user_items = set(items_df[items_df["user_id"] == user_id]["item_id"].values)

    #簡易スコア：近いユーザがどれだけ買っているか
    score = {}
    for ni, d in zip(neigh_idxs, neigh_dists):
        neigh_user = user_item_matrix.index[ni]
        neigh_items = set(items_df[items_df["user_id"] == neigh_user]["item_id"].values)

        # Distance -> Similarity
        sim = max(0.0, 1.0 - d)
        for item in neigh_items:
            if item in user_items:
                continue
            score[item] = score.get(item, 0.0) + sim

    #上位Top_kを返す
    ranked = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top_items = [iid for iid, _ in ranked[:top_k]]
    return item_master_df[item_master_df["item_id"].isin(top_items)][["item_id", "sex", "age", "type", "color"]]

print("User-based Recommendation:\n", recommend_for_user_based(user_id=10, top_k=5))

### === Notes ===
#1️⃣ アイテムベース推薦を動かす（すでにほぼ完成）
#	•	今の recommend_for_user 関数で、入力に購入アイテムのリストを与えると候補が出るようになっています。
#	•	改善案：item_id ではなく (sex, age, type, color) の情報を表示して、人間が読めるようにすると「おすすめの意味」がわかりやすくなります。
#
#⸻
#
#2️⃣ ユーザーベース推薦の導入
#	•	合成データを作成：
#	•	user_id（例: 1〜20人くらい）
#	•	item_id（1〜100）
#	•	timestamp（擬似的に購入時間をつける）
#	•	各ユーザーがランダムに数点購入した履歴を作成。
#	•	行列化して「ユーザー同士の類似度」を計算 → 似たユーザーが買っているアイテムを推薦。
#
#👉 このステップで「協調フィルタリングの2種類（アイテムベース / ユーザーベース）」を両方体験できます。
#
#⸻
#
#3️⃣ 評価指標を導入（Precision@5）
#	•	各ユーザーの最後の購入を「テスト用」に残して学習データから除外。
#	•	推薦結果の Top-5 にその購入アイテムが含まれている割合を計算。
#	•	Precision@5 = (ヒット数) / (ユーザー数) で簡単に実装できます。
#→ 実際のレコメンダー評価に近づけます。
#
#⸻
#
#4️⃣ モデルの比較実験
#	•	NearestNeighbors(metric="cosine") 以外に:
#	•	"euclidean"
#	•	"manhattan"
#	•	"jaccard"（scikit-learnでは直接ないので、バイナリ行列に変換して計算）
#	•	OneHotEncoder ではなく OrdinalEncoder を試す → どう変わるか比較。
#
#👉 「推薦の精度 × 距離関数 × 特徴量表現」でちょっとした研究ごっこができます。
#
#⸻
#
#5️⃣ Flet で GUI 化
#	•	シンプルな構成案：
#	•	左側：ユーザーが購入したアイテムを選ぶ（チェックボックス or ドロップダウン）
#	•	中央：k の値をスライダーで変更
#	•	右側：推薦結果をカード表示（アイテムIDと特徴をテキスト表示）
#	•	実装ヒント：
#	•	ft.Slider（k 値を調整）
#	•	ft.DataTable or ft.ListView（推薦結果の一覧表示）
#	•	on_change イベントで推薦結果を即時更新
