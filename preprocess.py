
import os, glob
import pandas as pd
from dateutil import parser
import numpy as np

RAW = "data/raw"
OUT = "data/cleaned"
os.makedirs(OUT, exist_ok=True)

def try_parse_time(col):
    # try to parse series to datetime
    try:
        s = pd.to_datetime(col, infer_datetime_format=True, errors="coerce")
        if s.notnull().sum() > 0:
            return s
    except:
        pass
    return None

for path in glob.glob(os.path.join(RAW, "*.parquet")):
    name = os.path.basename(path).replace(".parquet","")
    df = pd.read_parquet(path)
    print("Processing", name, "rows", len(df))

       df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]


    time_cols = [c for c in df.columns if any(k in c for k in ("time","date","timestamp","ts","created","logged"))]
    parsed = False
    for tc in time_cols:
        dtcol = try_parse_time(df[tc])
        if dtcol is not None and dtcol.notnull().sum() > 0:
            df["_ts"] = dtcol
            parsed = True
            break
    if not parsed:
               for c in df.columns[:3]:
            dtcol = try_parse_time(df[c])
            if dtcol is not None and dtcol.notnull().sum() > 0:
                df["_ts"] = dtcol
                parsed = True
                break

      for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()

       for c in df.columns:
        if df[c].dtype == "object":
            # try convert to numeric
            df[c+"_num"] = pd.to_numeric(df[c].str.replace(",",""), errors="coerce")

   
    df.to_parquet(os.path.join(OUT, f"{name}.parquet"), index=False)
    print("Saved cleaned:", name)
