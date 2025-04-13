import re
import time
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from models.schemas import WebArticle
from utils.llm import query_groq
from agents.query_analysis import analyze_query

def extract_keywords(text: str, top_k: int = 5):
    """
    Extracts the top_k most frequent keywords from the input text using counter.
    
    Parameters:
        text (str): The input text to extract keywords from.
        top_k (int): The number of top keywords to return.
    
    Returns:
        List[str]: A list of the most frequent keywords.
    """
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    word_counts = Counter(words)
    most_freq = word_counts.most_common(top_k)
    return [kw for kw, count in most_freq]


def is_accessible_content(text: str) -> bool:
    """
    Checks whether the text from a webpage is usable (i.e., not behind a login wall or too short).
    
    Parameters:
        text (str): The text content of a webpage.
    
    Returns:
        bool: True if content is accessible, otherwise False.
    """
    lower = text.lower()
    if "login" in lower or "sign in" in lower or "register to view" in lower:
        return False
    return len(text.strip()) > 100  # Avoid empty or near-empty pages

def web_scrape_with_selenium(query):
    """
    Uses Selenium to perform a web search on DuckDuckGo and scrape content from the top 3 accessible URLs.
    
    Parameters:
        query (str): The topic or subtopic to search for.
    
    Returns:
        Tuple[List[WebArticle], str]: 
            - List of structured WebArticle instances containing title, URL, summary, and keywords.
            - A combined summary (text) of up to 3 articles.
    """
    # Set up headless Chrome browser
    options = Options()
    options.add_argument('--headless') # No GUI
    options.add_argument('--no-sandbox') # Required for Linux environments
    options.add_argument('--disable-dev-shm-usage') # Improve performance on low-memory system
    driver = webdriver.Chrome(options=options)

    articles = []
    summaries = []
     
    try:
        # Open DuckDuckGo HTML-only search
        driver.get("https://html.duckduckgo.com/html/")
        # Enter the search query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        time.sleep(2)  # Allow time for results to load

        # Collect top search result links
        result_links = driver.find_elements(By.CSS_SELECTOR, "a.result__a")
        urls = [link.get_attribute("href") for link in result_links if link.get_attribute("href")]

        # Visit and extract info from top 3 URLs
        print(f"Found URLs: {urls[:3]}")

        for url in urls[:3]:
            try:
                driver.get(url)
                time.sleep(2)
                body_element = driver.find_element(By.TAG_NAME, "body")
                text = body_element.text.strip()
                # Skip if content is blocked or insufficient
                if not is_accessible_content(text):
                    print(f"Skipped {url} due to login wall or low content.")
                    continue

                # Create a short summary from the page body
                summary = text[:500] + "..." if len(text) > 500 else text
                keywords = extract_keywords(summary)
                title = driver.title or "Untitled"
                # Create a WebArticle and append
                article = WebArticle(
                    title=title,
                    url=url,
                    summary=summary,
                    keywords=keywords
                )
                articles.append(article)
                summaries.append(summary)
            except (TimeoutException, WebDriverException) as e:
                print(f"Skipped {url} due to error: {e}")

    finally:
        driver.quit() # Close the browser

    # Combine up to 3 summaries into one string
    final_summary = "\n".join(summaries[:3]) if summaries else "No accessible content found."

    return articles, final_summary
