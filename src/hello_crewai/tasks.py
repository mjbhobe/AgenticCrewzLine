from crewai import Task
from agents import researcher, editor
from tools import search_tool

research_task = Task(
    description="""
        Identify the next big trend in {topic}.
        Focus on identifying pros and cons and the overall narrative.
        Your final report should clearly articulate the key points,
        its market opportunities and potential risks.
    """,
    expected_output="""
        A comprehensive report on the latest trends in {topic}
    """,
    tools=[search_tool],
    agent=researcher,
)

edit_task = Task(
    description="""
        Compose an insightful article on {topic}.
        Focus on the latest trends and how it is impacting the industry.
        This article should be easy to understand, engaging and positive.
    """,
    expected_output="""
        A article, of approximately 5000 words, on {topic} advancements formatted as markdown file.
    """,
    tools=[search_tool],
    agent=editor,
    asynch_execution=False,
    output_file="news_blog_post.md",
)
