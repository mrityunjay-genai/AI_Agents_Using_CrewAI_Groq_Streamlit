import litellm
# Enable automatic parameter fixing for providers like Groq/Anthropic
litellm.modify_params = True 

import streamlit as st
from dotenv import load_dotenv
from src.utils import setup_stability_env, validate_environment

# 1. Setup Environment
load_dotenv()
setup_stability_env()

# 2. UI Header
st.set_page_config(page_title="Agent Research", page_icon="🔍")
st.title("🔍 Research Agent")

# 3. Validate keys before importing Crew logic
validate_environment()
from src.crew import ResearchCrew

topic = st.text_input("Enter Topic:")

if st.button("Start Research") and topic.strip():
    with st.spinner("Agent is working..."):
        try:
            result = ResearchCrew(topic).run()
            st.success("Done!")
            st.markdown(result.raw)
        except Exception as e:
            st.error(f"Error: {e}")
