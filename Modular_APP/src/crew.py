import os
from crewai import Agent, Task, Crew, LLM
from .tools import search_tool

class ResearchCrew:
    def __init__(self, topic):
        self.topic = topic
        self.llm = LLM(
            model="groq/openai/gpt-oss-120b",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.5,
            max_tokens=1000,
            tool_choice="auto"
        )

    def agent(self):
        return Agent(
            role="Research Specialist",
            goal=f"Thoroughly research {self.topic}",
            backstory=("Expert researcher specializing in data synthesis," 
                       "and Only use a tool if you are absolutely sure it is needed to answer the query. If you do not need a tool, respond with a direct text answer."),
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )

    def task(self, agent):
        return Task(
            description=(f"Analyze {self.topic} and provide a summary.,"
                         "You have access to a search tool. Use it only for factual queries you cannot answer from memory." ),
            agent=agent,
            expected_output="A comprehensive research summary."
        )

    def run(self):
        agent_instance = self.agent()
        crew = Crew(
            agents=[agent_instance],
            tasks=[self.task(agent_instance)],
            verbose=True
        )
        return crew.kickoff()
