import os
from dotenv import load_dotenv
from crew import FinancialAnalystCrew


# load all environment variables from .env file
load_dotenv()


def run():
    inputs = {
        # "company_name": "MSFT",
        "company_name": "TSLA",
        # "company_name": "Nvidia",
    }
    FinancialAnalystCrew("TSLA").crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
