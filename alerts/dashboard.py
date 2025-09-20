import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import pandas as pd

st.set_page_config(page_title="Anomaly Dashboard", layout="wide")
st.title("🚨 Real-Time Anomaly Alerts")

# Auto refresh every 2000 ms (2 sec)
st_autorefresh(interval=2000, limit=None, key="refresh")

# Ensure alerts.log exists
if not os.path.exists("alerts/alerts.log"):
    with open("alerts/alerts.log", "w", encoding="utf-8") as f:
        f.write("")

# Read alerts
with open("alerts/alerts.log", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# Show last 20 alerts
if lines:
    st.subheader("Latest Alerts")
    for line in lines[-20:]:
        st.error(line)

    # Parse for charts
    data = []
    for line in lines:
        if "User" in line:
            parts = line.split()
            try:
                user = parts[1]  # after "User"
                location = line.split("at")[-1].strip(". ")
                data.append({"user": user, "location": location})
            except Exception:
                continue

    if data:
        df = pd.DataFrame(data)

        st.subheader("📊 Alerts per User")
        st.bar_chart(df["user"].value_counts())

        st.subheader("🌍 Alerts per Location")
        st.bar_chart(df["location"].value_counts())

else:
    st.info("No alerts yet...")
