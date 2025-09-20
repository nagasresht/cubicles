import json
import os

def load_thresholds():
    """Load thresholds from config.json or return defaults"""
    config_path = os.path.join("alerts", "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Fallback defaults if file corrupted
            return {"login_threshold": 150, "data_transfer_threshold": 1000}
    return {"login_threshold": 150, "data_transfer_threshold": 1000}

def check_rules(event):
    """Apply rule-based anomaly detection"""
    thresholds = load_thresholds()
    anomalies = []

    # Rule 1: Login spike
    if event.get("logins_last_minute", 0) > thresholds["login_threshold"]:
        anomalies.append("Login spike detected")

    # Rule 2: Large data transfer
    if event.get("data_transfer_mb", 0) > thresholds["data_transfer_threshold"]:
        anomalies.append("Large data transfer")

    # Rule 3: Unusual login location (only allow common safe locations)
    if event.get("location") not in ["Delhi", "Mumbai", "USA"]:
        anomalies.append("Unusual login location")

    return anomalies
