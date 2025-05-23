from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

load_dotenv()
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")


async def main():
    async with sse_client(url="http://localhost:8000/sse") as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            # Discover available tools
            tools = await load_mcp_tools(session)
            print("Available tools:", tools)
            agent = create_react_agent(llm, tools)
            result = await agent.ainvoke(
                {
                    "messages": [
                        HumanMessage(
                            content="Research the company tavily whose url is https://tavily.com"
                        )
                    ]
                }
            )
            print("\nResearch Result:\n", result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
