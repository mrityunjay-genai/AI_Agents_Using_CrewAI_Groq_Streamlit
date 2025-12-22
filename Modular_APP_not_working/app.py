import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew

# Import our custom modules
from utils.agents import ResearchAgents
from utils.tasks import ResearchTasks

# Load Environment Variables
load_dotenv()

def run_app():
    st.set_page_config(page_title="Research Agent", page_icon="🔍")
    st.title("🔍 Research Agent (Modular)")

    # Validate Keys
    required_keys = ["SERPER_API_KEY", "GROQ_API_KEY", "GOOGLE_API_KEY"]
    if not all(os.getenv(k) for k in required_keys):
        st.error("❌ Missing API Keys in environment.")
        return

    topic = st.text_input("Enter the Research Topic:")

    if st.button("Run Research") and topic.strip():
        with st.spinner("Researching... Please wait."):
            try:
                # 1. Initialize our custom classes
                agents = ResearchAgents()
                tasks = ResearchTasks()

                # 2. Create the Agent and Task
                researcher = agents.research_specialist()
                research_task = tasks.conduct_research(researcher, topic)

                # 3. Form the Crew
                crew = Crew(
                    agents=[researcher],
                    tasks=[research_task],
                    verbose=True
                )

                # 4. Execute
                result = crew.kickoff()
                
                st.success("✅ Research Complete!")
                st.markdown("### Research Result")
                st.write(result.raw)

            except Exception as e:
                st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    run_app()
