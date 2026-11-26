import time
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_tavily import TavilySearch
import sqlite3
from dotenv import load_dotenv
import base64 

# 加载环境变量
load_dotenv()

# # 持久化记忆策略记忆
# connection = sqlite3.connect("resources/personal_chief.db", check_same_thread=False)
# checkpointer = SqliteSaver(connection)
# checkpointer.setup()

# prompt
system_prompt = """
你是一名私人厨师。收到用户提供的食材照片或清单后，请按以下流程操作：
1.识别和评估食材：若用户提供照片，首先辨识所有可见食材。基于食材的外观状态，评估其新鲜度与可用量，整理出一份“当前可用食材清单”。
2.智能食谱检索：优先调用 web_search 工具，以“可用食材清单”为核心关键词，查找可行菜谱。
3.多维度评估与排序：从营养价值和制作难度两个维度对检索到的候选食谱进行量化打分，并根据得分排序，制作简单且营养丰富的排名靠前。
4.结构化方案输出：把排序后的食谱整理为一份结构清晰的建议报告，要包含食谱信息、得分、推荐理由、食谱的参考图片，帮助用户快速做出决策。

请严格按照流程，优先调用 web_search 工具搜索食谱，搜索不到的情况下才能自己发挥。
"""

web_search = TavilySearch(
    max_results=5,
    topic="general",
)


# agent
model = ChatDeepSeek(
    model="deepseek-flash",  # 或 deepseek-reasoner
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
agent = create_agent(
    model=model, 
    system_prompt=system_prompt,
    tools=[web_search]
)

# config = {"configurable": {"thread_id": f"thread_{time.time()}"}}

# inputs = {
#     "messages": [
#         HumanMessage(
#             content=[
#                 {
#                     "type": "image",
#                     "url": "https://img.magnific.com/free-photo/arrangement-different-foods-organized-fridge_23-2149099882.jpg",
#                 }
#             ]
#         )
#     ]
# }

# response = agent.stream(inputs,config=config,stream_mode='messages')

# 
