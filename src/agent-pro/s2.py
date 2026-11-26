from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

load_dotenv()
# ==================== 1. 运行时上下文 ====================
@dataclass(frozen=True)
class UserContext:
    """Agent 运行时上下文"""

    user_id: str
    tenant_id: str


# ==================== 2. 模拟数据与常量 ====================
# 原代码里用到了 USER_DATABASE 但没有定义，这里补一份示例数据，请替换成你自己的
USER_DATABASE = {
    "school_a": {
        "u001": {"name": "张三", "course": "Python 进阶"},
    },
}

PREFERENCE_KEY = "learning_preferences"  # 固定的 key


def preference_namespace(ctx: UserContext) -> tuple[str, ...]:
    """根据 tenant_id 和 user_id 拼接 Store 的 namespace"""
    return ("heima_platform", ctx.tenant_id, ctx.user_id)


# ==================== 3. 工具 ====================
@tool
def get_current_user_profile(runtime: ToolRuntime[UserContext]) -> str:
    """查询当前登录用户的资料。"""
    ctx = runtime.context
    profile = USER_DATABASE.get(ctx.tenant_id, {}).get(ctx.user_id)

    if profile is None:
        return "未找到当前用户的资料"

    return f"姓名：{profile['name']}，课程：{profile['course']}"


@tool
def save_learning_preference(
    preference_name: str,
    preference_value: str,
    runtime: ToolRuntime[UserContext],
) -> str:
    """保存当前用户的长期学习偏好。"""
    namespace = preference_namespace(runtime.context)

    # 读出已有偏好（item.value 是 dict），没有就从空 dict 开始
    item = runtime.store.get(namespace, PREFERENCE_KEY)
    preferences = dict(item.value) if item else {}

    # 合并本次偏好后写回 Store
    preferences[preference_name] = preference_value
    runtime.store.put(namespace, PREFERENCE_KEY, preferences)

    return f"已保存偏好：{preference_name}={preference_value}"


@tool
def get_learning_preferences(runtime: ToolRuntime[UserContext]) -> str:
    """读取当前用户的长期学习偏好。"""
    namespace = preference_namespace(runtime.context)
    item = runtime.store.get(namespace, PREFERENCE_KEY)

    if item is None:
        return "当前用户还没有保存学习偏好"

    return f"当前学习偏好：{item.value}"


# ==================== 4. 创建 Agent ====================
checkpointer = InMemorySaver()  # 短期记忆：同一 thread 内的对话历史
store = InMemoryStore()  # 长期记忆：跨 thread 的用户偏好

agent = create_agent(
    model="deepseek-flash",
    tools=[
        get_current_user_profile,
        save_learning_preference,
        get_learning_preferences,
    ],
    context_schema=UserContext,
    checkpointer=checkpointer,
    store=store,
    system_prompt=(
        "你是课程平台助手。"
        "涉及用户资料时调用资料工具，"
        "涉及长期学习偏好或给用户讲解代码时调用偏好工具。"
    ),
)


# ==================== 5. 调用 ====================
if __name__ == "__main__":
    context = UserContext(user_id="u001", tenant_id="school_a")

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "记住：我喜欢先看代码，再看原理"}]},
        config={"configurable": {"thread_id": "thread-a"}},
        context=context,
    )

    for message in result["messages"]:
        message.pretty_print()
