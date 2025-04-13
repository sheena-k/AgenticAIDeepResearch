from typing import List, Dict
from pydantic import BaseModel # for output structuring & data validation


class WebArticle(BaseModel): # Stores core content from a single online source related to a subtopic
    title: str
    url: str
    summary: str
    keywords: List[str]

class ResearchSection(BaseModel): # Organizes multiple WebArticle instances that are all relevant to a specific sub-aspect of the overall topic.
    subtopic: str
    articles: List[WebArticle]

class ResearchReport(BaseModel): # Acts as the final deliverable combining all sections of research under the main topic.
    topic: str
    sections: List[ResearchSection]
