import streamlit as st
from src.utils import setup_environment, validate_environment
from src.agents import ResearchCrewManager

# 1. Init Environment and Logger
logger = setup_environment()

# print("hello")

# 2. UI Setup
st.set_page_config(page_title="InsightGen AI", page_icon="🔍", layout="wide")
st.title("🚀 Production Multi-Agent Research")
st.markdown("Automated technology research and content generation.")

# 3. Validation
serper_key, groq_key = validate_environment()

with st.sidebar:
    st.header("Settings")
    topic = st.text_input("Enter Research Topic:", placeholder="e.g., Quantum Computing")

if st.button("Run Research", type="primary") and topic.strip():
    with st.status("🤖 Agents collaborating...", expanded=False) as status:
        try:
            logger.info(f"Starting research on: {topic}")
            
            # Initialize Manager
            manager = ResearchCrewManager(topic, groq_key, serper_key)
            crew = manager.create_crew()
            
            # Execute
            result = crew.kickoff()
            
            st.success("✅ Analysis Complete")
            st.markdown("### 📝 Research Report")
            st.markdown(result.raw)
            
            st.download_button(
                label="Download Report as Markdown",
                data=result.raw,
                file_name=f"research_{topic.replace(' ', '_')}.md",
                mime="text/markdown"
            )
            status.update(label="Research complete!", state="complete", expanded=True)
            
        except Exception as e:
            logger.error(f"Critical Error: {str(e)}")
            st.error("An unexpected error occurred. Please check logs.")

elif not topic.strip():
    st.info("💡 Pro Tip: Enter a specific technology niche for better results.")
