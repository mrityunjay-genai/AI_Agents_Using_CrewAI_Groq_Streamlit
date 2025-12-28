import streamlit as st
from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import SerperDevTool

class ResearchCrewManager:
    def __init__(self, topic, groq_key, serper_key):
        self.topic = topic
        self.groq_key = groq_key
        self.serper_key = serper_key

    @st.cache_resource
    def _get_llm(_self):
        return LLM(
            model="groq/llama-3.3-70b-versatile",
            temperature=0.5,
            api_key=_self.groq_key,
            max_completion_tokens=400
        )

    @st.cache_resource
    def _get_tools(_self):
        return SerperDevTool(n_results=1, api_key=_self.serper_key)

    def create_crew(self):
        llm = self._get_llm()
        search_tool = self._get_tools()

        researcher = Agent(
            role="Senior Researcher",
            goal=f"Uncover groundbreaking technologies in {self.topic}",
            backstory="Driven by curiosity, you share innovation that changes the world.",
            tools=[search_tool],
            llm=llm,
            memory=True,
            verbose=True
        )

        writer = Agent(
            role="Writer",
            goal=f"Narrate compelling tech stories about {self.topic}",
            backstory="You simplify complex topics into engaging narratives.",
            tools=[search_tool],
            llm=llm,
            memory=True,
            verbose=True
        )

        task1 = Task(
            description=f"Identify the next big trend in {self.topic}. Focus on pros and cons.",
            expected_output="A comprehensive 3-paragraph report on latest trends.",
            agent=researcher
        )

        task2 = Task(
            description=f"Compose an insightful article on {self.topic} impacting the industry.",
            expected_output="A 4-paragraph markdown article.",
            agent=writer
        )

        return Crew(
            agents=[researcher, writer], 
            tasks=[task1, task2], 
            process=Process.sequential
        )
