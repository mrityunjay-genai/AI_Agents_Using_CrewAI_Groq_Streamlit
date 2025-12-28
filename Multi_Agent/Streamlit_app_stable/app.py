import streamlit as st
import os
import logging
from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv


# --- 1. Production Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY= os.getenv("GROQ_API_KEY")

if not SERPER_API_KEY or not GROQ_API_KEY:
    st.error("❌ Production Error: API keys missing in environment secrets.")
    st.stop()

# Environment Overrides
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

#  Cached Resource Initialization ---
@st.cache_resource
def get_llm():
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=GROQ_API_KEY,
        max_tokens=10,
        max_completion_tokens=400
    )

@st.cache_resource
def get_tools():
    return SerperDevTool(n_results=1, api_key=SERPER_API_KEY)

# --- 4. Agent and Task Logic ---
def create_crew(topic):
    llm = get_llm()
    search_tool = get_tools()
    
    researcher = Agent(
        role="Senior Researcher",
        goal=f"Uncover ground breaking technologies in {topic}",
        backstory="Driven by curiosity, you share innovation that could change the world.",
        tools=[search_tool],
        llm=llm,
        memory=True,
        verbose=True
    )
    
    writer = Agent(
        role="Writer",
        goal=f"Narrate compelling tech stories about {topic}",
        backstory="You simplify complex topics into engaging narratives.",
        tools=[search_tool],
        llm=llm,
        memory=True,
        verbose=True
    )
    
    task1 = Task(
        description=f"Identify the next big trend in {topic}. Focus on pros, cons, and market opportunities.",
        expected_output="A comprehensive 3-paragraph report on latest trends.",
        agent=researcher
    )
    
    task2 = Task(
        description=f"Compose an insightful article on {topic} impacting the industry.",
        expected_output="A 4-paragraph markdown article.",
        agent=writer
    )
    
    return Crew(agents=[researcher, writer], tasks=[task1, task2], process=Process.sequential)

# Streamlit UI ---
st.set_page_config(page_title="InsightGen AI", page_icon="🔍", layout="wide")

st.title("🚀 Production Multi-Agent Research")
st.markdown("Automated technology research and content generation.")

with st.sidebar:
    st.header("Settings")
    topic = st.text_input("Enter Research Topic:", placeholder="e.g., Quantum Computing")

if st.button("Run Research", type="primary") and topic.strip():
    with st.status("🤖 Agents collaborating...", expanded=False) as status:
        try:
            logger.info(f"Starting research on: {topic}")
            crew = create_crew(topic)
            result = crew.kickoff()
            
            st.success("✅ Analysis Complete")
            st.markdown("### 📝 Research Report")
            st.markdown(result.raw)
            
            # Offer download instead of just local saving (better for web production)
            st.download_button(
                label="Download Report as Markdown",
                data=result.raw,
                file_name=f"research_{topic.replace(' ', '_')}.md",
                mime="text/markdown"
            )
            status.update(label="Research complete!", state="complete", expanded=True)
            
        except Exception as e:
            logger.error(f"Critical Error: {str(e)}")
            st.error(f"An unexpected error occurred. Please contact support if this persists.")

elif not topic.strip():
    st.info("💡 Pro Tip: Enter a specific technology niche for better results.")
