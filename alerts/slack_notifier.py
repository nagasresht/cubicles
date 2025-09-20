import requests

WEBHOOK_URL = "https://hooks.slack.com/services/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"

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
