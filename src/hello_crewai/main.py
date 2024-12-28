from crew import crew


def main():
    """kick off crew with appropriate inputs & show results"""
    result = crew.kickoff(
        inputs={
            "topic": "Generative AI applications in Commercial Insurance Risk Assessment and Underwriting"
        }
    )
    print(result)


if __name__ == "__main__":
    main()
