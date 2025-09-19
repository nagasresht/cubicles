import streamlit as st

def update_dashboard(message):
    """
    Displays alert messages in a live dashboard.
    Run with: streamlit run alerts/dashboard.py
    """
    st.write(f"🚨 {message}")
