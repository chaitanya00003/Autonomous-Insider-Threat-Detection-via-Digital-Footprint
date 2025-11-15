

import os
import pandas as pd
from glob import glob

BASE_DIR = "data/r4.2" 

required_files = {
    "logon": "logon.csv",
    "http": "http.csv",
    "file": "file.csv",
    "email": "email.csv",
    "device": "device.csv"
}

parts = []

print("📌 Searching dataset in:", BASE_DIR)

for name, fname in required_files.items():
    fpath = os.path.join(BASE_DIR, fname)
    if os.path.exists(fpath):
        print(f"✅ Loading {fname}")
        df = pd.read_csv(fpath)
        df["source"] = name
        parts.append(df)
    else:
        print(f"❌ MISSING: {fname}")


ldap_files = glob(os.path.join(BASE_DIR, "LDAP", "*.csv"))
if ldap_files:
    print(f"✅ Loading {len(ldap_files)} LDAP files...")
    for lf in ldap_files:
        df = pd.read_csv(lf)
        df["source"] = "ldap"
        parts.append(df)
else:
    print("❌ No LDAP files found!")

if len(parts) == 0:
    raise SystemExit("🚫 No CSV files loaded! Check dataset path!")

print("✅ Merging all data...")
df_all = pd.concat(parts, ignore_index=True, sort=False)


ts_col = None
for col in df_all.columns:
    if col.lower() in ["time", "timestamp", "date", "event_time"]:
        ts_col = col
        break
if ts_col:
    df_all.rename(columns={ts_col: "timestamp"}, inplace=True)
else:
    print("⚠️ No timestamp column found")

print("✅ Final Shape:", df_all.shape)

os.makedirs("data/processed", exist_ok=True)
df_all.to_csv("data/processed/cert_all.csv", index=False)
print("✔ Saved → data/processed/cert_all.csv")
