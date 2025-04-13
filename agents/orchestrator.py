from agents.data_collector import web_scrape_with_selenium
from models.schemas import ResearchSection, ResearchReport
from agents.query_analysis import analyze_query
from utils.llm import query_groq

def generate_report(topic: str):
    """
    Generates a structured research report for a given topic using web scraping and LLM-based query analysis.

    Steps:
        1. Breaks down the input topic into subtopics-up to 3.
        2. For each subtopic, performs web scraping using Selenium to collect content from 3 relevant web pages.
        3. Summarizes and organizes the scraped content into structured report sections.
        4. Generates a final coherent response from the collected summaries using an LLM.

    Parameters:
        topic (str): The main topic for which research is to be conducted.

    Returns:
        Dict:
            {
                "report": ResearchReport,
                "scraped_data": List[Dict[str, str]],  # Each with 'url' and 'summary'
                "final_summary": str,  # LLM-generated coherent explanation
            }
    """

    subtopics = analyze_query(topic)[:3]
    report_sections = []
    all_articles = []
    all_summaries = []
    scraped_data = []

    for sub in subtopics:
        print(f"Searching for subtopic: {sub}")
        articles, _ = web_scrape_with_selenium(f"{topic} {sub}")

        if not articles:
            print(f"No articles found for subtopic: {sub}")
            continue

        # Collect summaries and raw data
        for article in articles:
            all_summaries.append(article.summary)
            scraped_data.append({
                "url": article.url,
                "summary": article.summary
            })
        
        all_articles.extend(articles)

        # Build section
        section = ResearchSection(
            subtopic=sub,
            articles=articles
        )
        report_sections.append(section)

    # Build LLM-based final summary
    merged_content = "\n".join([entry["summary"] for entry in scraped_data[:3]])
    final_summary = query_groq(
        f"Based on the following summaries, generate a coherent explanation in a structured and readable format:\n\n{merged_content}"
        ) if merged_content.strip() else "No accessible content found."

    # Return as structured dictionary
    return {"report": ResearchReport(topic=topic, sections=report_sections), "scraped_data": scraped_data,"final_summary": final_summary}
