import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew,LLM
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq

# --- Load environment variables --- 
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not SERPER_API_KEY or not GROQ_API_KEY or not GOOGLE_API_KEY:
    st.error("❌ Missing SERPER_API_KEY or GROQ_API_KEY or GOOGLE_API_KEY in your environment.")
    st.stop()

search_tool = SerperDevTool()


# 2. Use CrewAI's dedicated LLM class for Groq
llm_groq = LLM(
    model="groq/llama-3.3-70b-versatile",  # Specify provider prefix
    temperature=0.5,
    api_key=GROQ_API_KEY,
    max_tokens=1000 # Direct parameter in CrewAI's LLM class
)

def create_research_agent():
    return Agent(
        role="Research Specialist",
        goal="Conduct thorough research on a given topic",
        backstory=(
            "You are an experienced researcher with expertise in "
            "finding and synthesizing information from various sources."
        ),
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        llm=llm_groq
    )

def create_research_task(agent, topic):
    return Task(
        description=f"Research the following topic and provide a comprehensive summary: {topic}",
        agent=agent,
        # llm=llm_groq,
        expected_output=(
            "A detailed summary of the research findings, including key points and insights related to the topic."
        )
    )

def run_research(topic):
    agent = create_research_agent()
    task = create_research_task(agent, topic)
    crew = Crew(agents=[agent],
                tasks=[task])
    result = crew.kickoff()
    return result


# --- Streamlit UI ---
st.set_page_config(page_title="Research Agent", page_icon="🔍")
st.title("🔍 Research Agent (Groq-powered)")

st.markdown(
    """
    Enter a research topic below and let the AI agent find and summarize information for you!
    """
)

topic = st.text_input("Enter the Research Topic:")

if st.button("Run Research") and topic.strip():
    with st.spinner("Researching... Please wait."):
        try:
            result = run_research(topic)
            st.success("✅ Research Complete!")
            st.markdown("### Research Result")
            st.write(result.raw) # for Specially streamlit
        except Exception as e:
            st.error(f"❌ Error: {e}")
elif topic.strip() == "":
    st.info("Please enter a topic to start the research.")
