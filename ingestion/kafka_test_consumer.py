from kafka import KafkaConsumer
import json
import os

# Import anomaly detection modules
from detection.rules import check_rules
from detection.stats import check_stats
from explanation.llm_explainer import generate_explanation
from alerts.slack_notifier import send_slack_alert

# Create Kafka consumer
consumer = KafkaConsumer(
    "security-events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: m.decode("utf-8"),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="anomaly-detector"
)

print("✅ Listening for events with anomaly detection...")

# Ensure alerts folder exists
if not os.path.exists("alerts"):
    os.makedirs("alerts")

alerts_log = os.path.join("alerts", "alerts.log")

for message in consumer:
    raw_value = message.value
    try:
        event = json.loads(raw_value)  # Parse JSON event
    except json.JSONDecodeError:
        print("⚠️ Skipped non-JSON message:", raw_value)
        continue

    anomalies = []
    anomalies.extend(check_rules(event))
    anomalies.extend(check_stats(event))

    if anomalies:
        explanation = generate_explanation(event, anomalies)
        print("🚨 ALERT:", explanation)
        send_slack_alert(explanation)

        # 👇 Save alert to log file for dashboard
        with open(alerts_log, "a", encoding="utf-8") as f:
            f.write(explanation + "\n")
    else:
        print("✅ Normal event:", event)
