from datetime import datetime
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM,Process
from crewai_tools import SerperDevTool

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY= os.getenv("GROQ_API_KEY")

# Configuration
OUTPUT_DIR="/app/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.environ["OPENAI_API_KEY"]= "NA"

if not SERPER_API_KEY or not GROQ_API_KEY:
    raise EnvironmentError("MIssing SERPER_API_KEY or GROQ_API_KEY in your enviroment")

search_tool=SerperDevTool(n_results=1)
groq_model = "groq/llama-3.3-70b-versatile"
max_tokens=10

#CrewAI's dedicated LLM class for Groq 
llm_groq=LLM(
    model= groq_model,
    temperature=0.5,
    api_key=GROQ_API_KEY,
    max_tokens=max_tokens, # for testing
    max_completion_tokens=400
)

def create_research_agent():
    researcher_agent = Agent(
        role="Senior Researcher",
        goal="Uncover ground breaking technologies in {topic} ",
        backstory=("""Driven by curosity, you are at the forefront of innovation,
        eager to explore and share knowledge that could change the world
        """),
        tools=[search_tool],
        llm=llm_groq,
        allow_deligaton=True,
        memory=True,
        verbose=True
    )
    return researcher_agent

def create_writer_agent():
    write_agent = Agent(
        role="Writer",
        goal="Narrate compellng tech stories about {topic}",
        backstory=("""With a flair with smplifyng complex topics, you craft
        engaging narrative that captivate and enduce, bringing new discoveries to
        light in an accessible manner.
        """),
        tools=[search_tool],
        llm=llm_groq,
        allow_deligaton=True,
        memory=True,
        verbose=True
    )
    return write_agent

def create_research_task(reserch_agent,topic):
    research_task=Task(
        description=(f"""Identify the next big trend in {topic}.
        Focus on the identifying pros and cons and the overall narratve.
        Your final report should be clearly artculate the key points,
        its market opportunties and potential risks.
        """),
        expected_output= "A comprehensive 3 paragraphs long report on the latest AI trnds",
        tools=[search_tool],
        agent=reserch_agent,
    )
    return research_task

def create_wrter_task(writer_agent, topic):
    research_task=Task(
        description=(f"""Compose an insightfull article on {topic},
    Focus on the latest trends and how it's impacting the industry.
    This article should be easy to understand, engaging, and positive."""),
        expected_output= "A 4 pragraph article on {topic} advancements formeted as markdown",
        tools=[search_tool],
        agent=writer_agent,
        async_execution=False,
        output_file=f"{OUTPUT_DIR}/new_blog_post.md" # Primary output
    )
    return research_task



def run_all_agents(topic):
    reserch_agent= create_research_agent()
    research_task = create_research_task(reserch_agent,topic)

    writer_agent = create_writer_agent()
    writer_task = create_wrter_task(writer_agent,topic)
    crew=Crew(
        agents=[reserch_agent,writer_agent],
        tasks=[research_task, writer_task],
        # verbose=True,
        process=Process.sequential
    )
    result = crew.kickoff()
    return result
  

if __name__=="__main__":
    print("welcome to the Multiagent Demo!")
    topic="AI in healthcare"
    response = run_all_agents(topic)
    print("Research Result:\n")
    print(response)
    # Inside multi_agent.py
    
    # getting time
    now = datetime.now()
    formatted_time = now.strftime("%H:%M:%S")
    print("Current Time =", formatted_time)
    # # Backup: Manual write to ensure persistence
    with open(f"{OUTPUT_DIR}/generated_file.md", "w") as f:
        f.write(f"{str(response)}\n{formatted_time}")
    print(f"Results written to {OUTPUT_DIR}")


