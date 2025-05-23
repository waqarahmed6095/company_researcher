from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from backend.graph import Graph
import asyncio
import logging
import uuid
from langchain_core.messages import HumanMessage
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# Create an MCP server
mcp = FastMCP("company-researcher-mcp")

@mcp.tool()
async def research_company(company_name: str, company_url: str) -> str:
    """
    Research a company and give the content in output
    Args:
        company_name: The name of the company to research
        company_url: The url of the company to research
    Returns:
        The content of the company research in markdown format
    """
    try:
        output_format = "markdown"
        mcp=True
        graph = Graph(company=company_name, url=company_url, output_format=output_format,mcp=mcp)
        workflow = graph.compile()
        

        thread = {"configurable": {"thread_id": str(uuid.uuid4())}}

        # Run the graph and collect progress
        content = await workflow.ainvoke(graph.state, thread)

        # Return all progress messages joined, or just the last one
        return content
    except Exception as e:
        return f"Error researching company: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse")
    




