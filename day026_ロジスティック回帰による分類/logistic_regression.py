# logistic_regression.py

### Imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

rng = np.random.default_rng(42)

# パラメータ（自分で色んな数値を入力し、理解を深める）
n_users = 1000
lam_visits = 3.0
beta0 = -2.0
beta1 = 0.6