from crewai import Task

class ResearchTasks:
    def conduct_research(self, agent, topic):
        return Task(
            description=f"Research the following topic and provide a comprehensive summary: {topic}",
            agent=agent,
            expected_output=(
                "A detailed summary of the research findings, including key points and insights."
            )
        )
