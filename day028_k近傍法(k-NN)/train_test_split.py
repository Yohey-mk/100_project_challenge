# train_test_split.py

from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

### === 0. Get prepared ===
def get_dfs():
    items_df = pd.read_csv("user_purchses.csv")
    return items_df

### === 1. train/test split ===
def train_test_split_by_user(items_df, test_size=0.2, random_state=42):
    train_records, test_records = [], []
    for uid, group in items_df.groupby("user_id"):
        items = group["item_id"].tolist()
        if len(items) < 2:
            #データが少なすぎる場合はすべてtrainへ
            train_records.extend(group.to_dict("records"))
            continue
        train_items, test_items = train_test_split(items, test_size=test_size, random_state=42)
        train_records.extend(group[group["item_id"].isin(train_items)].to_dict("records"))
        test_records.extend(group[group["item_id"].isin(test_items)].to_dict("records"))
    return pd.DataFrame(train_records), pd.DataFrame(test_records)

items_df = get_dfs()

train_df, test_df = train_test_split_by_user(items_df, test_size=0.2)

### === 2. trainデータでUser-Item行列を作成, 推薦関数（train用）===
class UserBasedRecommender:
    def __init__(self, train_df, item_master_df, n_neighbors=6, metric="cosine"):
        self.train_df = train_df
        self.item_master_df = item_master_df
        self.user_item_matrix = pd.crosstab(train_df["user_id"], train_df["item_id"])
        self.nn = NearestNeighbors(n_neighbors=n_neighbors, metric=metric).fit(self.user_item_matrix)
        self.distances, self.indices = self.nn.kneighbors(self.user_item_matrix)

    def recommend(self, user_id, top_k=5, with_attributes=True):
        if user_id not in self.user_item_matrix.index:
            return []
        
        idx = self.user_item_matrix.index.get_loc(user_id)
        neigh_idxs = self.indices[idx][1:]
        neigh_dists = self.distances[idx][1:]
        user_items = set(self.train_df[self.train_df["user_id"] == user_id]["item_id"].values)

        score = {}
        for ni, d in zip(neigh_idxs, neigh_dists):
            neigh_user = self.user_item_matrix.index[ni]
            neigh_items = set(self.train_df[self.train_df["user_id"] == neigh_user]["item_id"].values)
            sim = max(0.0, 1.0 - d)
            for item in neigh_items:
                if item in user_items:
                    continue
                score[item] = score.get(item, 0.0) + sim

        ranked = sorted(score.items(), key=lambda x: x[1], reverse=True)
        top_items = [iid for iid, _ in ranked[:top_k]]
    
        if with_attributes:
            return self.item_master_df[self.item_master_df["item_id"].isin(top_items)][
                ["item_id", "sex", "age", "type", "color"]
            ].reset_index(drop=True)
        else:
            return top_items


### === 3. Precision@k 計算 ===
def precision_at_k(recommender, test_df, user_id, k=5):
    test_items = set(test_df[test_df["user_id"] == user_id]["item_id"].values)
    if len(test_items) == 0:
        return None
    
    recommended_items = recommender.recommend(user_id, top_k=k, with_attributes=False)
    if len(recommended_items) == 0:
        return None
    
    hits = len(set(recommended_items) & test_items)
    return hits / k

def mean_precision_at_k(recommender, test_df, k=5, max_users=None):
    precisions = []
    for i, uid in enumerate(test_df["user_id"].unique()):
        if max_users and i >= max_users:
            break
        p = precision_at_k(recommender, test_df, uid, k)
        if p is not None:
            precisions.append(p)
    return np.mean(precisions) if precisions else 0.0

