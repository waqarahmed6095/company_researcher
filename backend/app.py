# app.py
import asyncio
from .graph import Graph

async def main():
    # Initialize the Graph
    graph = Graph()

    company_name = "Tavily" # Replace with the desired company name
    company_url = "https://tavily.com/" # Replace with the desired company URL

    # Specify output format; defaults to "pdf" if not specified.
    output_format = "pdf"  # Change to "markdown" if desired or leave it as an optional argument


    # Run the graph for a specific company and URL
    await graph.run(company=company_name, url=company_url, output_format=output_format)

if __name__ == "__main__":
    asyncio.run(main())
