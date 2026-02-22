# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# 1. データの読み込み
print("データを読み込んでいます...")
df = pd.read_csv("student_placement_prediction_dataset_2026.csv")

# 2. 特徴量（X）とターゲット（y）の選択
# 予測のヒントに使う「数値データ」のカラムを複数選んでXに代入する。
features = ['cgpa', 'coding_skill_score', 'aptitude_score', 'communication_skill_score',
            'logical_reasoning_score', 'mock_interview_score',
            'college_tier', 'branch', 'internships_count'
            ]

X = df[features]

# 予測したい正解データ（今回は就職状況）のカラム名をyに代入する
y = df['placement_status']

# 2.1 カテゴリ変数の数値化（One-Hot Encoding）
# pandasのget_dummies()関数を使って文字データを0/1のデータに変換する
X_endoded = pd.get_dummies(X, drop_first=True) # drop_first=Trueは統計学的エラー（多重共線性）を防ぐためのおまじない

# 3. データの分割（学習用とテスト用に分ける）
# train_test_splitを使ってX_encodedとyを8:2の割合に分割 *Xではなくカテゴリ変数を数値化したX_encodedを使うのがポイント
# test_size=0.2とすると、20%がテスト用に回される
X_train, X_test, y_train, y_test = train_test_split(X_endoded, y, test_size=0.2, random_state=42)

# 4. モデルの準備と学習
print("AIモデルを学習中...")
# RandomForestClassifierのモデルを準備する
model = RandomForestClassifier(random_state=42)
# 学習データ（X_train, y_train）を使って、モデルにパターンを学習（fit）させる
model.fit(X_train, y_train)

# 5. 予測と評価
# テストデータ（X_test）を使って予測を行う
predictions = model.predict(X_test)

# 実際の正解（y_test）と予測結果を比べて精度を確認する
accuracy = accuracy_score(y_test, predictions)

print(f"モデルの予測精度（Accuracy）：{accuracy * 100:.2f}%")