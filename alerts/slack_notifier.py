import requests

WEBHOOK_URL = "<your_slack_webhook_url>"

def send_slack_alert(message):
    """
    Sends anomaly alerts to Slack channel via webhook.
    """
    if WEBHOOK_URL.startswith("<your"):
        print("⚠️ Slack webhook not configured. Printing alert instead.")
        print("SLACK ALERT:", message)
        return

    payload = {"text": message}
    requests.post(WEBHOOK_URL, json=payload)
