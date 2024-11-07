from tavily import AsyncTavilyClient
from langchain_openai import ChatOpenAI
import os 

from dotenv import load_dotenv
load_dotenv('.env')

# Set Your API Keys
TAVILY_API_KEY= os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")



# Initialize Tavily Async client 
tavily_client = AsyncTavilyClient(api_key= TAVILY_API_KEY)

# Initialize OpenAI models for research tasks and final generation
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
final_model = ChatOpenAI(model="gpt-4o", temperature=0)