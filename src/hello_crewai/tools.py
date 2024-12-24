from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# setup search tool
search_tool = SerperDevTool()
