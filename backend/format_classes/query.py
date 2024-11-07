from pydantic import BaseModel, Field
from typing import List

# Add Tavily's arguments to enhance the web search tool's capabilities
class TavilyQuery(BaseModel):
    query: str = Field(description="web search query")
    topic: str = Field(description="type of search, should be 'general' or 'news'. Choose 'news' ONLY when the company you searching is publicly traded and is likely to be featured on popular news")
    days: int = Field(description="number of days back to run 'news' search")
 

# Define the args_schema for the tavily_search tool using a multi-query approach, enabling more precise queries for Tavily.
class TavilySearchInput(BaseModel):
    sub_queries: List[TavilyQuery] = Field(description="set of sub-queries that can be answered in isolation")
