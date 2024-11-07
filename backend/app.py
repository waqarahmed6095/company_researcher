# app.py
import asyncio
from .graph import Graph

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

async def main():
    # Initialize the Graph
    graph = Graph()
    
    # Run the graph for a test company and URL
    await graph.run(company="Tavily", url="https://tavily.com/")
    
    # Print the result
    # print("Graph Execution Result:", type(result))

if __name__ == "__main__":
    asyncio.run(main())
