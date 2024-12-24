import sys, os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# load keys from .env file
load_dotenv()

print(f"GOOGLE_API_KEY: {os.getenv("GOOGLE_API_KEY")}")
print(f"SERPER_API_KEY: {os.getenv("SERPER_API_KEY")}")
print(f"COMET_API_KEY (should fail!): {os.getenv("COMET_API_KEY")}")
