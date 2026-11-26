from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.agents import AgentState
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


# 定义自定义State结构
class CustomState(AgentState):
    """Agent的任务状态"""

    model_call_count: int  # 模型调用次数


@tool
def update_model_call_count(runtime: ToolRuntime):
    """A tool that count model call"""

    # 获取state中的数据
    count = runtime.state.get("model_call_count", 0)
    print("model_call_count:", count)

    # 更新State数据
    update = {
        "model_call_count": count + 1,
        "messages": [
            ToolMessage(
                content="Successfully updated agent state",
                tool_call_id=runtime.tool_call_id,
            )
        ],
    }

    return Command(update=update)


agent = create_agent(
    "deepseek-flash",
    tools=[update_model_call_count],
    state_schema=CustomState,  # 告诉Agent使用自定义的state
    checkpointer=InMemorySaver(),
    system_prompt="你是AI助手，你需要调用工具记录模型调用次数",
)


config = {"configurable": {"thread_id": "1"}}
response = agent.invoke({"messages": [HumanMessage(content="Hi,我是虎哥")]}, config)

for message in response["messages"]:
    message.pretty_print()


response = agent.invoke({"messages": [HumanMessage(content="还记得我是谁吗")]}, config)

for message in response["messages"]:
    message.pretty_print()

print(agent.get_state(config))