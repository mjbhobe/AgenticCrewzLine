from crewai import Agent
from crewai_tools import SerperDevTool

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chat_models import ChatOpenAI
import litellm
import os

from tools import search_tool
from dotenv import load_dotenv

load_dotenv()

# define my LLM - we'll be using Gemini LLM (as it's free, so far!!)
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     temperature=0.5,
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     verbose=True,
# )

# above does not work - try the following
# @see: https://chiraggarg09.medium.com/implementing-crewai-a-deep-dive-into-llm-integration-challenges-6786e594a968

# os.environ["OPENAI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
litellm.api_key = os.getenv("GOOGLE_API_KEY")

# llm = ChatOpenAI(
#     model_name="gemini/gemini-1.5-flash",  # Note the provider prefix
#     temperature=0.6,
#     openai_api_key=os.getenv("GOOGLE_API_KEY"),
#     max_tokens=1000,
#     verbose=True,
# )

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
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
