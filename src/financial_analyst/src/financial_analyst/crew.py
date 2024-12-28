from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task

from langchain_community.chat_models import ChatOpenAI
import litellm
import os
from dotenv import load_dotenv

from tools.calculator_tool import CalculatorTool
from tools.sec_tools import SEC10KTool, SEC10QTool

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

load_dotenv()

# NOTE: I am NOT using OpenAI LLM, but Google Gemini instead (because API if free!)
# however, the conventional way of creating the Gemini LLM (as shown commented below)
# does not work, so we use the alternate way of creating the Gemini LLM

# conventional way of createing instance of ChatGoogleGenerativeAI
# Does NOT work with CrewAI :(

# from langchain_google_genai import ChatGoogleGenerativeAI
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     temperature=0.5,
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     verbose=True,
# )

# here is the alternative way of creating my LLM, which works!
# @see: https://chiraggarg09.medium.com/implementing-crewai-a-deep-dive-into-llm-integration-challenges-6786e594a968

# os.environ["OPENAI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
litellm.api_key = os.getenv("GOOGLE_API_KEY")

# gemini_flash = ChatOpenAI(
#     model_name="gemini/gemini-1.5-flash",  # Note the provider prefix
#     temperature=0.6,
#     openai_api_key=os.getenv("GOOGLE_API_KEY"),
#     max_tokens=1000,
#     verbose=True,
# )

from langchain_google_genai import ChatGoogleGenerativeAI

gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    verbose=True,
)


# create the crew
@CrewBase
class FinancialAnalystCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, company_symbol: str) -> None:
        self.llm = gemini_flash
        self.company_symbol = company_symbol

    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["company_researcher"],
            llm=self.llm,
            # verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                SEC10QTool(self.company_symbol),
                SEC10KTool(self.company_symbol),
            ],
        )

    @agent
    def company_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["company_analyst"],
            llm=self.llm,
            # verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                # WebsiteSearchTool(),
                SEC10QTool(self.company_symbol),
                SEC10KTool(self.company_symbol),
            ],
        )

    @task
    def company_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_company_task"],
            agent=self.company_researcher(),
        )

    @task
    def analyze_company_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_company_task"],
            agent=self.company_analyst(),
            output_file=f"financial_analysis_{self.company_symbol}.md",
        )

    @crew
    def crew(self) -> Crew:
        """creates the Financial Analyst Crew"""
        return Crew(
            agents=self.agents,  # automated created
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
