import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


model = init_chat_model(
    model="deepseek-v4-flash", extra_body={"thinking": {"type": "disabled"}}
)


async def main():

    # client = MultiServerMCPClient(
    #     {
    #         "time": {
    #             "transport": "stdio",
    #             "command": "uvx",
    #             "args": ["mcp-server-time", "--local-timezone=Asia/Shanghai"],
    #         }
    #     }
    # )

    client = MultiServerMCPClient(
        {
            "kiwi-com-flight-search": {
                "transport": "http", 
                "url": "https://mcp.kiwi.com"
            }
        }
    )

    tools = await client.get_tools()

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="You are a travel agent. Help user find best flights. No follow up questions. If the user uses Chinese, use zh-cn as the locale value.",
    )

    response = await agent.ainvoke(
        {"messages": [HumanMessage("查一下2026年11月22日晚上从北京飞杭州的航班。")]}
    )

    # print(response)
    for message in response["messages"]:
        message.pretty_print()

if __name__ == "__main__":
    asyncio.run(main())
