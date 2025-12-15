import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler, RobustScaler, OrdinalEncoder, PowerTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
import joblib

# 1 — Load data
data = pd.read_csv("../raw_data/train.csv")
data_test = pd.read_csv("../raw_data/test.csv")

X = data.drop(columns=['loan_paid_back', 'id'])
y = data['loan_paid_back']

numeric = ["annual_income", "debt_to_income_ratio", "credit_score",
           "loan_amount", "interest_rate"]

categorical = ["gender", "marital_status", "education_level",
               "employment_status", "loan_purpose", "grade_subgrade"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
])

model = Pipeline([
    ("preprocess", preprocessor),
    ("svc", SVC(probability=True))  # kernel=rbf by default
])

# 3 — Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4 - Grid Search

param_grid = {
    "svc__C": [0.1, 1, 10],
    "svc__kernel": ["rbf", "poly", "linear"],
    "svc__gamma": ["scale", "auto"]
}

grid = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,
    scoring="roc_auc",
    n_jobs=-1,
    verbose=1   # optional, prints progress
)

print("Running GridSearchCV…")
grid.fit(X_train, y_train)

print("Best params:", grid.best_params_)
print("Best CV ROC AUC:", grid.best_score_)


# -----------------------
# 4. Evaluate the best model
# -----------------------

best_model = grid.best_estimator_

# Accuracy
test_accuracy = best_model.score(X_test, y_test)
print("\nTest Accuracy:", test_accuracy)

# ROC AUC with predict_proba
y_pred_proba = best_model.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, y_pred_proba)
print("Test ROC AUC:", test_auc)

# -----------------------
# 5. Save best model
# -----------------------

joblib.dump(best_model, "svc_best_model.joblib")
print("\n💾 Saved best model to svc_best_model.joblib")
