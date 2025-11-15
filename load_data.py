import os
import pandas as pd

SRC = "r4.2"
OUT = "data/raw"
os.makedirs(OUT, exist_ok=True)

def read_and_save(path, out_name):
    try:
        df = pd.read_csv(path, low_memory=False)
        df.to_parquet(os.path.join(OUT, out_name + ".parquet"), index=False)
        print("Saved:", out_name, "rows:", len(df))
    except Exception as e:
        print("Failed to read", path, ":", e)


top_files = ["file.csv","http.csv","logon.csv","psychometric.csv","email.csv","device.csv"]
for fn in top_files:
    p = os.path.join(SRC, fn)
    if os.path.exists(p):
        read_and_save(p, fn.replace(".csv",""))

ldap_dir = os.path.join(SRC, "LDAP")
if os.path.isdir(ldap_dir):
    combined = []
    for fn in sorted(os.listdir(ldap_dir)):
        if fn.endswith(".csv"):
            p = os.path.join(ldap_dir, fn)
            try:
                df = pd.read_csv(p, low_memory=False)
                df["__source_file"] = fn
                combined.append(df)
                print("Read LDAP:", fn, "rows:", len(df))
            except Exception as e:
                print("Failed LDAP file", fn, ":", e)
    if combined:
        ldap_all = pd.concat(combined, ignore_index=True, sort=False)
        ldap_all.to_parquet(os.path.join(OUT, "ldap_all.parquet"), index=False)
        print("Saved combined LDAP rows:", len(ldap_all))


for txt in ["readme.txt","license.txt"]:
    p = os.path.join(SRC, txt)
    if os.path.exists(p):
        with open(p,"r",encoding="utf-8",errors="ignore") as f:
            content = f.read(4000)
        with open(os.path.join(OUT, txt), "w", encoding="utf-8") as fo:
            fo.write(content)
        print("Wrote snippet of", txt)
