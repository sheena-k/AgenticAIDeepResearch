from agents.orchestrator import generate_report
from utils.llm import query_groq

def main():
    """
    Main function for conducting deep research on a given topic, generating a structured report,
    and producing a coherent explanation by synthesizing the findings using a language model.

    Steps:
    1. Prompts the user for a topic to conduct research.
    2. Calls the `generate_report` function to generate a structured research report.
    3. Displays URLs and corresponding summaries from web scraping.
    4. Shows the final LLM-generated explanation.
    """
    # User Query
    topic = input("Enter a topic for deep research: ")

    # Generate research data
    result = generate_report(topic)

    # Extract results
    report = result["report"]
    scraped_data = result["scraped_data"]
    final_summary = result["final_summary"]
    
    # Display Report
    print(f"\n report:{report}")
    
    # Display scraped URLs and summaries
    print("\n Scraped URLs and Summaries: \n")
    for item in scraped_data:
        print(f"URL: {item['url']}")
        print(f"Summary: {item['summary']} \n")

    # Display final summary
    print("\n Final Summary:\n ")
    #print(final_summary)
    # Use LLM to generate a final combined response based on the summaries AND original query
    final_response = query_groq(
    f"""User Query: {topic}
    Using the following information gathered from various sources, give a detailed and coherent explanation that directly answers the query above:
    {final_summary}
    """
    )
    print(final_response)


if __name__ == "__main__":
    main()
