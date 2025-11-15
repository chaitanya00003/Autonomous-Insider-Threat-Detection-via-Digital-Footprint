
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

ALERTS = "outputs/alerts.csv"
FEAT = "data/features/features_user_day.parquet"

st.set_page_config(page_title="Insider Threat Dashboard", layout="wide")
st.title("🚨 Insider Threat Detection — Advanced Dashboard")

if not os.path.exists(ALERTS):
    st.error("No alerts found. Run detect.py first.")
    st.stop()

alerts = pd.read_csv(ALERTS)
alerts["_date"] = pd.to_datetime(alerts["_date"])

st.sidebar.header("Filters")
users = st.sidebar.multiselect("User", sorted(alerts["user_id"].unique().astype(str)), default=[])
min_ml = st.sidebar.slider("Min ML score", float(alerts["ml_score"].min()), float(alerts["ml_score"].max()), float(alerts["ml_score"].min()))
rule_only = st.sidebar.checkbox("Show rule-based alerts only", value=False)

df = alerts.copy()
if users:
    df = df[df["user_id"].isin(users)]
df = df[df["ml_score"] >= min_ml]
if rule_only:
    df = df[df["rule_flag"]==1]

c1, c2, c3 = st.columns(3)
c1.metric("Total Alerts", len(alerts))
c2.metric("Filtered Alerts", len(df))
c3.metric("Unique Users Alerted", df["user_id"].nunique())

st.subheader("Recent Alerts")
st.dataframe(df.sort_values("_date", ascending=False).head(200), use_container_width=True)


st.subheader("Alerts Over Time")
time_df = df.groupby(df["_date"].dt.date).size().reset_index(name="count")
fig = px.bar(time_df, x="_date", y="count", title="Alerts per Day")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Users by Avg ML Score")
user_stats = df.groupby("user_id")["ml_score"].mean().reset_index().sort_values("ml_score", ascending=False)
fig2 = px.bar(user_stats.head(20), x="user_id", y="ml_score", title="Avg ML Score by User")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Scatter: total_bytes vs ml_score")
if "total_bytes" in df.columns:
    fig3 = px.scatter(df, x="total_bytes", y="ml_score", color="user_id", hover_data=["user_id"])
    st.plotly_chart(fig3, use_container_width=True)

st.download_button("Download filtered alerts (CSV)", df.to_csv(index=False), "alerts_filtered.csv", "text/csv")
