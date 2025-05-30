import re
from utils.llm import query_groq  

def analyze_query(topic: str):
    """
    Breaks down a given research topic into 3 subtopics using an LLM-based query agent.

    This function sends a prompt to a language model (via `query_groq`) to extract major subtopics 
    for deeper exploration. The response is expected as a list (one subtopic per line), which is 
    then cleaned and returned.

    Parameters:
        topic (str): The main topic to be analyzed.

    Returns:
        List[str]: A cleaned list of 3 subtopics suitable for further web-based research.
    """
    prompt = f"Break down the topic '{topic}' into 3 major subtopics for deep web-based research. Return the result as a list."
    result = query_groq(prompt)
    if not result:
        return []
    return [re.sub(r'^\s*[\d\-\.\)]*\s*', '', line.strip()) for line in result.split('\n') if line.strip()]


