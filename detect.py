
import os, json, csv
import pandas as pd
import numpy as np
import joblib
from datetime import date, datetime

FEAT = "data/features/features_user_day.parquet"
os.makedirs("outputs", exist_ok=True)

df = pd.read_parquet(FEAT)

meta = joblib.load("models/iso_model.joblib")
iso = meta["model"]
FEATURES = meta["features"]
scaler = joblib.load("models/scaler.joblib")
th = json.load(open("models/threshold.json"))
THRESH = th["threshold"]

X = df[FEATURES].fillna(0).astype(float).values
Xs = scaler.transform(X)
ml_scores = -iso.decision_function(Xs)

rules = []
for i, r in df.iterrows():
    rule = 0
    if r.get("total_bytes", 0) > df["total_bytes"].quantile(0.95):
        rule = 1
    if (
        (r.get("remote_vm_count", 0) > 0)
        and (r.get("unknown_loc_count", 0) > 0)
        and (r.get("sftp_count", 0) > 0)
    ):
        rule = 1
    rules.append(rule)
rules = np.array(rules)

alerts_idx = np.where((ml_scores > THRESH) | (rules == 1))[0]

alerts = []
for idx in alerts_idx:
    row = df.iloc[idx].to_dict()
    alert = {
        k: row.get(k)
        for k in [
            "user_id",
            "_date",
            "total_bytes",
            "avg_hour",
            "sftp_count",
            "remote_vm_count",
            "unknown_loc_count",
        ]
    }
    alert["ml_score"] = float(ml_scores[idx])
    alert["rule_flag"] = int(rules[idx])

    # ✅ Convert date or datetime objects to string
    if isinstance(alert.get("_date"), (datetime, date)):
        alert["_date"] = alert["_date"].isoformat()

    alerts.append(alert)

def convert_dates(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

with open("outputs/alerts.json", "w") as f:
    json.dump(alerts, f, indent=2, default=convert_dates)

out_csv = "outputs/alerts.csv"
pd.DataFrame(alerts).to_csv(out_csv, index=False)
print("✅ Alerts saved:", out_csv, "Count:", len(alerts))
