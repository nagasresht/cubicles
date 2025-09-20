import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import pandas as pd
from datetime import datetime
import json

st.set_page_config(page_title="Anomaly Dashboard", layout="wide")
st.title("🚨 Real-Time Anomaly Alerts")

# --- Sidebar Config Panel ---
st.sidebar.header("⚙️ Detection Thresholds")

login_threshold = st.sidebar.slider("Login Spike Threshold (logins/minute)", 50, 300, 150)
data_transfer_threshold = st.sidebar.slider("Data Transfer Threshold (MB)", 100, 5000, 1000)

# Ensure alerts folder exists
if not os.path.exists("alerts"):
    os.makedirs("alerts")

config_path = os.path.join("alerts", "config.json")

# Save thresholds to config.json every refresh
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(
        {
            "login_threshold": login_threshold,
            "data_transfer_threshold": data_transfer_threshold
        },
        f,
        indent=2
    )

# --- Auto Refresh every 2 sec ---
st_autorefresh(interval=2000, limit=None, key="refresh")

# Ensure alerts.log exists
alerts_log = os.path.join("alerts", "alerts.log")
if not os.path.exists(alerts_log):
    with open(alerts_log, "w", encoding="utf-8") as f:
        f.write("")

# Read alerts
with open(alerts_log, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

if lines:
    st.subheader("Latest Alerts")

    # --- Color-coded alerts ---
    for line in lines[-20:]:
        if line.startswith("[HIGH]"):
            st.error(line)   # red
        elif line.startswith("[MEDIUM]"):
            st.warning(line) # orange/yellow
        elif line.startswith("[LOW]"):
            st.info(line)    # blue
        else:
            st.write(line)

    # --- Parse data for charts ---
    data = []
    for line in lines:
        if "User" in line:
            parts = line.split()
            try:
                user = parts[1]  # username after "User"
                location = line.split("at")[-1].strip(". ")
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")  # group by minute

                # Extract severity
                if line.startswith("[HIGH]"):
                    severity = "HIGH"
                elif line.startswith("[MEDIUM]"):
                    severity = "MEDIUM"
                elif line.startswith("[LOW]"):
                    severity = "LOW"
                else:
                    severity = "UNKNOWN"

                data.append({
                    "user": user,
                    "location": location,
                    "timestamp": ts,
                    "severity": severity
                })
            except Exception:
                continue

    if data:
        df = pd.DataFrame(data)

        # 📊 Alerts per User
        st.subheader("📊 Alerts per User")
        st.bar_chart(df["user"].value_counts())

        # 🌍 Alerts per Location
        st.subheader("🌍 Alerts per Location")
        st.bar_chart(df["location"].value_counts())

        # 📈 Alerts Over Time
        st.subheader("📈 Alerts Over Time (per minute)")
        time_counts = df.groupby("timestamp").size()
        st.line_chart(time_counts)

        # 🥧 Severity Breakdown
        st.subheader("🟢 Severity Breakdown")
        st.bar_chart(df["severity"].value_counts())

else:
    st.info("No alerts yet...")
