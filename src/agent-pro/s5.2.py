import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import os

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": [os.path.join(os.path.dirname(__file__),'s5.1.py')],  
            }
        }
    )

    tools = await client.get_tools()

    agent = create_agent(
        model="deepseek-flash",
        tools=tools,
        system_prompt="You are a helpful agent. You must use tools to answer math question.",
    )

    response = await agent.ainvoke(
        {"messages": [HumanMessage("467和529的平方根之和是多少?")]}
    )
    for message in response["messages"]:
        message.pretty_print()
    
    
if __name__ == '__main__':
    asyncio.run(main())