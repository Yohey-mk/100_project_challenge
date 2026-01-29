# decision_tree_and_random_forest.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import shap
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Study source
# https://www.kaggle.com/code/olehantemeniuk/system-analysis-feature-importance-shap

# Titanic dataを取得
#df = fetch_openml("heart-disease-uci", version=1, as_frame=True).frame
df = pd.read_csv("heart_disease_uci.csv")

df.rename(columns={'age': 'Age', 'sex': 'Sex', 'trestbps': 'RestingBP', 'chol': 'Cholesterol',
                   'thalch': 'MaxHR', 'oldpeak': 'Oldpeak',
                   'num': 'HeartDisease', 'cp': 'ChestPainType'}, inplace=True)

drop_cols = ['id', 'dataset']
for col in drop_cols:
    if col in df.columns:
        df = df.drop(columns=[col])

if 'HeartDisease' in df.columns:
    df['HeartDisease'] = df['HeartDisease'].apply(lambda x: 1 if x > 0 else 0)
else:
    print("Warning: 'HeartDisease' column not found.")
    print(df.columns)

if 'id' in df.columns:
    df = df.drop(columns=['id'])

# Data cleaning
numeric_columns = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 欠損値の処理
print(f"Missing values before drop:\n{df.isnull().sum()}")
df.dropna(inplace=True)
print(f"Dataset shape after cleanup: {df.shape}")
print(f"Column names: {list(df.columns)}")
print(f"First few rows:")
print(df.head())

# create a copy for encoding
df_encoded = df.copy()

# Enode categorical columns
le = LabelEncoder()
categorical_cols = df_encoded.select_dtypes(include=['object', "string"]).columns

for col in categorical_cols:
    df_encoded[col] = le.fit_transform(df_encoded[col])

print(f"Encoded categorical columns: {list(categorical_cols)}")
print(f"\nEncoded dataset:")
df_encoded.head()

# Separate features and target
X = df_encoded.drop('HeartDisease', axis=1)
y = df_encoded['HeartDisease']

print(f"Target classes: {y.unique()}")

# Split into train and test sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape[0]} samples")
print(f"Test set size: {X_test.shape[0]} samples")
print(f"Number of feature: {X_train.shape[1]}")
print(f"\nFeature names: {list(X.columns)}")

# Initialize and train the RFC model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate model accuracy
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy on Test Set: {accuracy:.4f}")

# Create SHAP explainer for the trained model
explainer = shap.TreeExplainer(model)

# Calculate SHAP values for the test set
shap_values = explainer.shap_values(X_test)

if isinstance(shap_values, list):
    shap_values_to_plot = shap_values[1]
else:
    shap_values_to_plot = shap_values
    if len(shap_values.shape) == 3:
        shap_values_to_plot = shap_values[:, :, 1]

plt.figure()
shap.summary_plot(shap_values_to_plot, X_test, show=False)
plt.tight_layout()
plt.show()
print("SHAP values calculated successfully.")
print(f"SHAP values shape: {shap_values_to_plot.shape}")
print(type(shap_values))
print(np.array(shap_values).shape)

plt.figure()
plt.title("Average Feature Importance (Mean SHAP value)")
shap.summary_plot(shap_values_to_plot, X_test, plot_type="bar", show=False)
plt.tight_layout()
plt.show()

# Calculate feature importance based on mean absolute SHAP values
feature_importance = pd.DataFrame({
    'feature': X_test.columns,
    'importance': np.abs(shap_values_to_plot).mean(axis=0)
}).sort_values('importance', ascending=False)

print("Top 10 Most Important Features:")
print(feature_importance.head(10))

# Get top 3 features for dependence plots
top_features = feature_importance['feature'].head(3).tolist()
print(f"\nCreateing dependence plots for: {top_features}")

# Dependence plot for the most important feature
if len(top_features) > 0:
    plt.figure(figsize=(8,5))
    shap.dependence_plot(top_features[0], shap_values_to_plot, X_test, interaction_index=None, show=False)
    plt.title(f"Risk Dependence on {top_features[0]}")
    plt.tight_layout()
    plt.show()

# Dependence plot for the second most important feature
if len(top_features) > 1:
    plt.figure(figsize=(8,5))
    shap.dependence_plot(top_features[1], shap_values_to_plot, X_test, interaction_index="auto", show=False)
    plt.title(f"Risk Dependence on {top_features[1]}")
    plt.tight_layout()
    plt.show()

# Dependence plot for the third most important feature
if len(top_features) > 2:
    plt.figure(figsize=(8,5))
    shap.dependence_plot(top_features[2], shap_values_to_plot, X_test, interaction_index="auto", show=False)
    plt.title(f"Risk Dependence on {top_features[2]}")
    plt.tight_layout()
    plt.show()

# Waterfall plot for the first patient in the test set
# 1. Base Value (基準値/平均値)の取得
# ランダムフォレストは[Class0の平均、Class1の平均]のリストを持っているため、
# Class 1(病気あり)の平均値だけと取り出す
if isinstance(explainer.expected_value, list) or isinstance(explainer.expected_value, np.ndarray):
    base_value = explainer.expected_value[1]
else:
    base_value = explainer.expected_value[0]

# 2. Explanationオブジェクトを手動で作成
# すでに集計済みのshap_values_to_plot(Class 1専用)を再利用。
# これにより"Type Error"を回避
explanation = shap.Explanation(
    values=shap_values_to_plot,
    base_values=base_value,
    data=X_test.values,
    feature_names=X_test.columns
)

# 3. 最初の患者さんのWaterfall Plotを表示
# E[f(x)] (下部にある数値): 全患者の平均的なリスク（基準値）
# f(x) (上部にある数値): この患者さんの最終的な予測スコア（確率）。
print("\nGenerating Waterfall plot for the first patient")
plt.figure()
# explanation[0]で最初の患者さんのデータを指定
shap.plots.waterfall(explanation[0], show=False)
plt.tight_layout()
# 赤色の矢印はリスクを押し上げた要因（悪い要素）、青いのは押し下げた要因（良い要素）
plt.show()

# 4. Waterfall plots for patients 2 and 3
plt.figure()
shap.plots.waterfall(explanation[1], show=False)
plt.title("Prediction Explanation for patient #2")
plt.tight_layout()
plt.show()

plt.figure()
shap.plots.waterfall(explanation[2], show=False)
plt.title("Prediction Explanation for patient #3")
plt.tight_layout()
plt.show()
