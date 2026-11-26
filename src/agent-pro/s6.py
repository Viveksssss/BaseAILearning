import asyncio
import sys
import warnings
import sqlite3

if sys.platform == "win32":
    if "ipykernel" in sys.modules:
        sys.stderr = sys.__stderr__


from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain.agents import AgentState
from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain.tools import ToolRuntime
from langchain.messages import HumanMessage, ToolMessage, AIMessage
from langgraph.types import Command
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()


async def main():
    # MCP客户端，包含Time、Kiwi两个MCP

    client = MultiServerMCPClient(
        {
            "travel_server": {"transport": "http", "url": "https://mcp.kiwi.com"},
            
            "time": {
                "transport": "stdio",
                "command": "uvx",
                "args": [
                    "--with",
                    "tzdata",
                    "mcp-server-time",
                    "--local-timezone=Asia/Shanghai",
                ],
            },
        }
    )

    tools = await client.get_tools()

    travel_agent = create_agent(
        model="deepseek-flash",
        tools=tools,
        system_prompt="""
        你是一个旅行助手Agent。你为用户搜索到达婚礼地点的理想航班，您不能再追问任何后续问题。
        您必须根据以下标准找到最佳航班选择：
        - 价格（最低，经济舱）
        - 持续时间（最短）
        - 日期（您认为在该地点举行婚礼的最佳时间）
        为了使事情变得简单，只寻找一张票，单程。
        你不会得到额外的信息，只有出发地和目的地。你的工作是批判性地思考最佳选择。
        一旦你找到了最好的选项，让用户知道你的候选列表。
        调用搜索航班工具时，如果是地点在中国，需要使用zh-cn作为Locale参数。
        """,
    )

    # 定义Tavily web_search工具
    web_search = TavilySearch(
        max_results=5,
        topic="general",
    )

    # 创建 Venue agent
    venue_agent = create_agent(
        model="deepseek-flash",
        tools=[web_search],
        system_prompt="""
        你是场地专家，你在指定的位置搜索满足要求的场地。
        你不能再追问任何后续问题，你必须根据以下标准找到最佳的场地选择：
        - 价格（最低）
        - 容量（完全匹配）
        - 评价（最高）
        您可能需要进行多次搜索以迭代地找到最佳选项。
        """,
    )

    @tool
    def query_playlist_db(query: str) -> str:
        """Query the database for playlist information"""

        try:
            with sqlite3.connect(r"E:\Code\python\base\resources\Chinook.db") as conn:
                rows = conn.execute(query).fetchall()
            return str(rows)
        except Exception as e:
            return f"Error querying database: {e}"

    # Playlist agent
    playlist_agent = create_agent(
        model="deepseek-flash",
        tools=[query_playlist_db],
        system_prompt="""
        你是播放列表专家。查询sql数据库并为给定类型的婚礼策划完美的播放列表。
        一旦你有了你的播放列表，计算播放列表的总时长和成本，每首歌都有一个相关的价格。
        如果在查询数据库时遇到错误，请尝试通过更改查询来修复它们。
        不要空手而归，继续尝试查询数据库，直到你找到一个歌曲列表。
        您可能需要进行多个查询以迭代地找到最佳选项。
        """,
    )

    class WeddingState(AgentState):
        origin: str  # 起点
        destination: str  # 目的地
        guest_count: str  # 宾客数量
        genre: str  # 婚礼风格

    @tool
    def update_state(
        origin: str,
        destination: str,
        guest_count: str,
        genre: str,
        runtime: ToolRuntime,
    ) -> str:
        """当你询问用户，知道下列所有值时更新State：origin、destination、guest_count、genre"""
        return Command(
            update={
                "origin": origin,
                "destination": destination,
                "guest_count": guest_count,
                "genre": genre,
                "messages": [
                    ToolMessage(
                        "Successfully updated state", tool_call_id=runtime.tool_call_id
                    )
                ],
            }
        )

    @tool
    async def search_flights(runtime: ToolRuntime) -> str:
        """旅行Agent搜索飞往理想婚礼地点的航班."""
        origin = runtime.state["origin"]
        destination = runtime.state["destination"]

        content = f"查询从{origin}到{destination}的航班"
        response = await travel_agent.ainvoke({"messages": [HumanMessage(content)]})
        return response["messages"][-1].content

    @tool
    def search_venues(runtime: ToolRuntime) -> str:
        """场地Agent根据给定的地点和宾客数量寻找最佳的婚礼场地."""
        destination = runtime.state["destination"]
        capacity = runtime.state["guest_count"]

        content = f"在{destination}寻找适合{capacity}宾客的婚礼场地"
        response = venue_agent.invoke({"messages": [HumanMessage(content)]})
        return response["messages"][-1].content

    @tool
    def suggest_playlist(runtime: ToolRuntime) -> str:
        """播放列表Agent根据类型风格策划完美的播放列表."""
        genre = runtime.state["genre"]

        content = f"策划符合{genre}风格的婚礼播放列表的曲目"
        response = playlist_agent.invoke({"messages": [HumanMessage(content)]})
        return response["messages"][-1].content

    coordinator = create_agent(
        model="deepseek-flash",
        tools=[search_flights, search_venues, suggest_playlist, update_state],
        state_schema=WeddingState,
        system_prompt="""
        你是婚礼协调员。你负责与用户沟通，找到更新状态所需的所有信息，并更新到state。
        一旦完成，你就可以委派任务了。将查找航班、搜索场地和策划播放列表的任务委派给您的专家Agent。
        当你收到他们的答案，为我设计一场完美的婚礼方案。
        """,
    )

    async for mode, chunk in coordinator.astream(
        {
            "messages": [
                HumanMessage(
                    content="我来自北京，我想在上海举办一场100人的婚礼，爵士风格的。"
                )
            ],
        },
        stream_mode=["updates", "messages", "custom"],  # 必须是列表
    ):
        if mode == "messages":
            # 逐 token 输出，只显示协调员模型生成的文字
            token, meta = chunk
            if token.content and meta.get("langgraph_node") == "model":
                print(token.content, end="", flush=True)
        elif mode == "updates":
            # 每个节点（model / tools）完成时打印一行进度
            for node, update in chunk.items():
                print(f"\n[完成节点: {node}]", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
