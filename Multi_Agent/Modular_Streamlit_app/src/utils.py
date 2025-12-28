import os
import logging
import litellm
import streamlit as st
from dotenv import load_dotenv

def setup_environment():
    # Setup Logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    # Load Env
    load_dotenv()

    # 2025 Stability Tweaks
    litellm.modify_params = True 
    os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
    os.environ["OTEL_SDK_DISABLED"] = "true"
    
    return logger

def validate_environment():
    """Validates keys and stops the app if missing."""
    serper = os.getenv("SERPER_API_KEY")
    groq = os.getenv("GROQ_API_KEY")
    
    if not serper or not groq:
        st.error("❌ Production Error: API keys missing in environment secrets.")
        st.stop()
    return serper, groq
