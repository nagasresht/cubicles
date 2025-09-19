def generate_explanation(event, anomalies):
    """
    Generate a simple human-friendly explanation.
    (Later: connect to OpenAI/LLM here)
    """
    user = event.get("user", "unknown")
    location = event.get("location", "unknown")
    explanation = f"User {user} triggered anomalies {anomalies} at {location}."
    return explanation
