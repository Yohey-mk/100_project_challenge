# train_model_v3.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import plotly.express as px
import joblib

print("Dataを読み込んでいます...")
df = pd.read_csv("student_placement_prediction_dataset_2026.csv")

# 1. すべての特徴量を使ってXを作る。
# ただし使わない列をDropしてXを作成する。（例：student_id、salary_package、placement_status(予測したい正解そのもの)など）
X = df.drop(columns=['student_id', 'salary_package_lpa', 'placement_status'])
y = df['placement_status']

# 2. カテゴリ変数の数値化（One-Hot Encoding）
# 全部のデータを対象にget_dummiesをかける
X_encoded = pd.get_dummies(X, drop_first=True)

# 3. データの分割
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# 4. モデルの準備と学習
print("総当りでAIモデルを学習させています...")
model = RandomForestClassifier(
    random_state=42,
    max_depth=10,
    min_samples_split=50)
model.fit(X_train, y_train)

# 5. 予測と評価
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"データ総当りの予測精度(Accuracy):{accuracy * 100:.2f}%")

# 6. AIがどのデータを重視したか？の数値を取り出す（Feature Importance）
importance = model.feature_importances_

# 見やすくするためにDataFrameにまとめる
importance_df = pd.DataFrame({
    'Feature': X_encoded.columns,
    'Importance': importance
})

# 重要度が高い順に並び替えする
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Plotlyで可視化してみる
fig = px.bar(
    importance_df.head(10),
    x='Importance',
    y='Feature',
    title='To 10 Feature Importances(AIが重視したデータ)',
    orientation='h'
)

# グラフのレイアウトを整える
fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.show()

# モデルをファイルに保存する
print("学習したAIをファイルに保存しています...")
# joblib.dump()を使ってmodelをrf_model.pklという名前で保存する
joblib.dump(model, 'rf_model.pkl', compress=3)
# X_c=encodedのカラム名（列の順番）もAIにとっては重要なので、一緒に保存する
joblib.dump(X_encoded.columns.tolist(), 'model_columns.pkl')

print("保存完了！'rf_model.pkl'と'model_columns.pkl'が作成されました。")