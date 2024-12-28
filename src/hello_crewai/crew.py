from crewai import Crew, Process
from agents import researcher, editor
from tasks import research_task, edit_task

crew = Crew(
    agents=[researcher, editor],
    tasks=[research_task, edit_task],
    process=Process.sequential,
)
