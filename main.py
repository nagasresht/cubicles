from ingestion.file_reader import read_stream
from detection.rules import check_rules
from detection.stats import check_stats
from explanation.llm_explainer import generate_explanation
from alerts.slack_notifier import send_slack_alert
# from alerts.dashboard import update_dashboard  # optional

def main():
    print("🚀 Cyber Anomaly Detector Started...")

    # Example: read events one by one
    for event in read_stream("data/mock_logins.csv"):
        anomalies = []
        anomalies.extend(check_rules(event))
        anomalies.extend(check_stats(event))

        if anomalies:
            explanation = generate_explanation(event, anomalies)
            print("ALERT:", explanation)
            send_slack_alert(explanation)
            # update_dashboard(explanation)  # optional

if __name__ == "__main__":
    main()
