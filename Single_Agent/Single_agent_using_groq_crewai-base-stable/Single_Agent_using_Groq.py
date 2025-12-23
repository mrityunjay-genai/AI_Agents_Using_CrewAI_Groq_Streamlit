import concurrent.futures.process  # Force early registration of atexit handlers
import litellm

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew,LLM
from crewai_tools import SerperDevTool

# Load environment variables
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

os.environ["OPENAI_API_KEY"] = "NA"

if not SERPER_API_KEY or not GROQ_API_KEY:
    raise EnvironmentError("Missing SERPER_API_KEY or GROQ_API_KEY in your environment.")

search_tool = SerperDevTool(n_results=1)


# 2. Use CrewAI's dedicated LLM class for Groq
llm_groq = LLM(
    model= "groq/llama-3.3-70b-versatile",##"groq/llama-3.1-8b-instant",    #"groq/llama-3.3-70b-versatile",  # Specify provider prefix
    temperature=0.5,
    api_key=GROQ_API_KEY,
    max_tokens=100 # Direct parameter in CrewAI's LLM class
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
                tasks=[task],
                verbose=True,
                # cache=True #Use the cache=True parameter on your Crew to prevent redundant API calls for identical tasks.
                )
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    print("Welcome to the Research Agent!")
    # topic = input("Enter the Research Topic: ")
    topic="Gen ai"
    response = run_research(topic)
    print("Research Result:\n")
    print(response)