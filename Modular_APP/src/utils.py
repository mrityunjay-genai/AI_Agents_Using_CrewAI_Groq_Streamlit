import os
import streamlit as st

def setup_stability_env():
    """Sets global flags to prevent threading crashes and telemetry noise."""
    os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
    os.environ["OTEL_SDK_DISABLED"] = "true"
    os.environ["LITELLM_LOG"] = "ERROR"

def validate_environment():
    """Checks for required API keys."""
    required = ["SERPER_API_KEY", "GROQ_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        msg = f"❌ Missing keys: {', '.join(missing)}"
        st.error(msg)
        st.stop()
