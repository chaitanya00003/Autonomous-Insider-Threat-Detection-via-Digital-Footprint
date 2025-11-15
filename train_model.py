# train_model.py
import os, json
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

FEAT = "data/features/features_user_day.parquet"
os.makedirs("models", exist_ok=True)

df = pd.read_parquet(FEAT)

# apply simple pre-filter to remove extremely anomalous rows before training
mask = ~((df["total_bytes"] > df["total_bytes"].quantile(0.99)) | ((df["remote_vm_count"]>0) & (df["unknown_loc_count"]>0)))
train_df = df[mask]

FEATURES = ["total_bytes","avg_hour","sftp_count","remote_vm_count","unknown_loc_count"]
X = train_df[FEATURES].fillna(0).astype(float).values

scaler = StandardScaler()
Xs = scaler.fit_transform(X)

iso = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
iso.fit(Xs)

# compute anomaly score (higher => more anomalous)
scores = -iso.decision_function(Xs)
threshold = float(np.percentile(scores, 99))

joblib.dump({"model":iso,"features":FEATURES}, "models/iso_model.joblib")
joblib.dump(scaler, "models/scaler.joblib")
with open("models/threshold.json","w") as f:
    json.dump({"threshold": threshold, "features": FEATURES}, f, indent=2)

print("Trained model saved. threshold:", threshold)
