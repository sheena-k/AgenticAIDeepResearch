### Implementation of an Agentic Deep Research System  


#### Goal:   

**To build a modular, end-to-end research agent framework that leverages multiple agents to conduct deep research and generate structured reports. The focus is on using Pydantic-ai for output structuring and validation, along with open-source tools for search and scraping.**  



#### System Architecture:  

**Query Analysis Agent:**

    Breaks down user queries into structured sub-tasks.
    
**Web Search & Data Collection Agent:**

    Conducts web searches and scrapes relevant data to fulfill the subtasks.
    
**Orchestration Agent:**

    Manages the workflow and ensures smooth communication between agents.  



#### Framework and Tools:  

    Pydantic-ai for schema enforcement, output structuring and strict validation across components.
    
    Open-source Models from Groq for natural language understanding and text generation.
    
    Web Tools for search and scraping- selenium.


#### File structire    

Agents --->>

    data_collector.py
    
    orchestration.py
    
    query_analysis.py
    
models --->>

    schemas.py
    
utils --->>

    llm.py
