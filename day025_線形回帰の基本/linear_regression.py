# linear_regression.py

### === Imports ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sys
import os

### === Functions ===
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys.MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def data_loader(filename="study_score_data.csv"):
    path = resource_path(filename)
    df = pd.read_csv(path, encoding="utf-8")
    return df

#モデルの作成と学習
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

def visualize(X, y, model, X_new, y_pred):
    X_sorted = np.sort(X, axis=0)
    plt.scatter(X, y, color="blue", label="Training data")
    plt.plot(X_sorted, model.predict(X_sorted), color="red", label="Regression line")
    plt.scatter(X_new, y_pred, color="green", label="Prediction (x=9)")
    plt.legend()
    plt.show()


# Data
study_data = data_loader()
X = np.array(study_data['study_hours']).reshape(-1, 1) # 2D化
y = np.array(study_data['score'])

#予測
model = train_model(X, y)
X_new = np.array([[9], [1], [14], [12]])
y_pred = model.predict(X_new)

print("Predictions: ", y_pred)
print("Coefficient (slope):", model.coef_[0])
print("Intercept:", model.intercept_)

# Visualize
visualize(X, y, model, X_new, y_pred)