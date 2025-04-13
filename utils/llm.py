from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv("agent_venv/.env") 
def query_groq(prompt: str):

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",   # llm model called using Groq API key for language understanding and context generation
        messages=[
            {"role": "system", "content": "You are a helpful assistant who gives coherent, clear, and accurate answers.."},
            {"role": "user", "content":prompt}
        ],
        max_tokens=300,  # limit length
        temperature=0.3  # randomness
    )
    return response.choices[0].message.content

