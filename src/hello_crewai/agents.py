from crewai import Agent
from crewai_tools import SerperDevTool

from langchain_google_genai import ChatGoogleGenerativeAI
import os

from tools import search_tool

# define my LLM - we'll be using Gemini LLM (as it's free, so far!!)
llm = ChatGoogleGenerativeAI(
    model="gemini/gemini-1.5-flash",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    verbose=True,
)


# senior research agent
researcher = Agent(
    role="Senior Researcher",
    goal="Uncover groundbreaking technologies in {topic}",
    backstory="""
        Driven by technology you are at the forefront of innovation,
        eager to explore and share knowledge that could change the world!
    """,
    memory=True,
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    llm=llm,
)

# editor agent with custom tools
editor = Agent(
    role="News writer",
    goal="Narrate compelling stories about {topic}",
    backstory="""
        With a flair for simplifying complex topics, you craft
        engaging narratives that captivate and educate, bringing
        new discoveries to light in an accessible manner        
    """,
    memory=True,
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm,
)
