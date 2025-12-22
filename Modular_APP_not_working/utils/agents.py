import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool

# Disable telemetry before CrewAI imports
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

class ResearchAgents:
    def __init__(self):
        self.search_tool = SerperDevTool()
        self.llm = LLM(
            model="groq/llama-3.3-70b-versatile",
            temperature=0.5,
            api_key=os.getenv("GROQ_API_KEY"),
            max_tokens=500
        )

    def research_specialist(self):
        return Agent(
            role="Research Specialist",
            goal="Conduct thorough research on a given topic",
            backstory=(
                "You are an experienced researcher with expertise in "
                "finding and synthesizing information from various sources."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool],
            llm=self.llm
        )
