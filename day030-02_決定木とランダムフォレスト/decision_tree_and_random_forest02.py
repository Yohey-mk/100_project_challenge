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