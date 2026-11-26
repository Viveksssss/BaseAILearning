# # # from dotenv import load_dotenv
# # # from langchain.messages import HumanMessage
# # # from langchain.agents import create_agent
# # # from langchain.agents.middleware import PIIMiddleware
# # # from langchain.agents.middleware import ModelFallbackMiddleware
# # # load_dotenv()
# # # # =================1.定义PIIMiddleware==========================
# # # # 也可以添加多个PII中间件来检测不同类型的敏感信息
# # # pii_middleware_email = PIIMiddleware(
# # #     "email", strategy="redact", apply_to_input=False, apply_to_output=True  # mask
# # # )

# # # pii_middleware_phone = PIIMiddleware(
# # #     "phone_number",
# # #     # 使用自定义正则表达式
# # #     detector=r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}",
# # #     strategy="hash",
# # #     apply_to_input=True,
# # # )

# # # model_fallback_middleware = ModelFallbackMiddleware(
# # #     "deepseek-v", "deepseek-flash"  # 默认模型  # 备用模型
# # # )

# # # # ====================2.在Agent中注册PIIMiddleware================
# # # agent_with_builtin_middleware = create_agent(
# # #     model="deepseek-flash", middleware=[pii_middleware_email, pii_middleware_phone,model_fallback_middleware]
# # # )


# # # # ======================3.测试=================================
# # # response = agent_with_builtin_middleware.invoke(
# # #     {
# # #         "messages": [
# # #             HumanMessage(
# # #                 "我的邮箱是: huge@itcast.cn,我的电话是13698023405,你要记住这些信息，后续要用到。如果记住了请确认一遍。"
# # #             )
# # #         ]
# # #     }
# # # )
# # # for m in response["messages"]:
# # #     m.pretty_print()


# # # emails = [
# # #     {
# # #         "subject": "周末见个面？",
# # #         "content": """
# # #                 嗨 虎哥，
# # #                 我下周会去城里，不知道我们有没有机会一起喝杯咖啡？

# # #                 祝好，简
# # #             """,
# # #         "from": "jane@itcast.cn",
# # #         "status": "unread",
# # #     },
# # #     {
# # #         "subject": "周五会议",
# # #         "content": """
# # #                 嗨 虎哥，
# # #                 非常抱歉，我周五的会议无法准时参加了，能不能重新安排个时间？

# # #                 祝好，小李
# # #             """,
# # #         "from": "lixiaolong@itcast.cn",
# # #         "status": "checked",
# # #     },
# # # ]
# # # from dotenv import load_dotenv
# # # from langchain.tools import tool
# # # from langchain.agents import create_agent
# # # from langgraph.checkpoint.memory import InMemorySaver
# # # from langchain.messages import HumanMessage

# # # # 定义工具，收取和发送邮件
# # # @tool
# # # def check_inbox() -> str:
# # #     """查看收件箱中的邮件."""

# # #     # 模拟收件箱邮件
# # #     return emails


# # # @tool
# # # def send_email(to: str, subject: str, body: str) -> str:
# # #     """发送回复邮件"""
# # #     return f"邮件已发送至 {to} , 主题： {subject} , 内容： {body}"

# # # load_dotenv()

# # # from langchain.agents.middleware import HumanInTheLoopMiddleware,before_agent,after_agent,after_model,before_model,wrap_model_call,wrap_tool_call

# # # # 创建人工审核中间件
# # # human_in_loop_middleware = HumanInTheLoopMiddleware(
# # #     interrupt_on={
# # #         "send_email": {
# # #             "description": "请确认邮件内容",
# # #             "allowed_decisions": ["approve", "reject", "edit"],
# # #         }
# # #     }
# # # )


# # # agent_with_hitl = create_agent(
# # #     model="deepseek-flash",
# # #     tools=[check_inbox, send_email],
# # #     middleware=[human_in_loop_middleware],
# # #     checkpointer=InMemorySaver(),
# # #     system_prompt="你是一个邮件助手",
# # # )


# # # config = {"configurable": {"thread_id": "1"}}
# # # response = agent_with_hitl.invoke(
# # #     {"messages": [HumanMessage("帮我查看邮件")]}, config=config
# # # )

# # # for message in response["messages"]:
# # #     message.pretty_print()


# # # response = agent_with_hitl.invoke(
# # #     {"messages": [HumanMessage("帮我回复Jane，很高兴她能来，问问她具体见面时间")]},
# # #     config=config
# # # )
# # # for message in response["messages"]:
# # #     message.pretty_print()


# # # from langgraph.types import Command

# # # response = agent_with_hitl.invoke(
# # #     Command(
# # #         resume={
# # #             "decisions": [
# # #                 {
# # #                     "type": "reject",  # 人工确认的决定，是reject
# # #                     "message": "语气太书面了，Jane是我的女朋友！",  # 请求被拒绝的原因
# # #                 }
# # #             ]
# # #         }
# # #     ),
# # #     config=config,  # 相同的thread_id以恢复暂停的对话
# # # )

# # # for message in response["messages"]:
# # #     message.pretty_print()


# # # response = agent_with_hitl.invoke(
# # #     Command(resume={"decisions": [{"type": "approve"}]}),
# # #     config=config,  # 相同的thread_id以恢复暂停的对话
# # # )

# # # for message in response["messages"]:
# # #     message.pretty_print()


# # # from typing import Any, Callable
# # # from dotenv import load_dotenv
# # # from langchain.tools import tool
# # # from langchain.agents import create_agent
# # # from langgraph.checkpoint.memory import InMemorySaver
# # # from langchain.messages import HumanMessage
# # # from langchain.agents.middleware import after_model
# # # from langchain.agents import AgentState
# # # from langgraph.runtime import Runtime
# # # from langchain.agents.middleware import wrap_model_call
# # # from langchain.agents.middleware import ModelRequest,ModelResponse

# # # class CustomState(AgentState):
# # #     """扩展Agent状态，添加自定义字段"""

# # #     model_call_count: int  # 模型调用次数


# # # load_dotenv()


# # # @wrap_model_call
# # # def retry_model(
# # #     request:ModelRequest,
# # #     handler:Callable[[ModelRequest],ModelResponse]
# # # )->ModelResponse:
# # #     for attm in range(3):
# # #         try:
# # #             return handler(request)
# # #         except Exception as e:
# # #             print(f'Retry {attm+1} / 3 after error:{e}')
# # #             if attm == 2:
# # #                 raise

# # #     return None


# # # @after_model(state_schema=CustomState)
# # # def increment_counter(state: CustomState, runtime: Runtime) -> dict[str, Any]:
# # #     current_counter = state.get("model_call_count", 0)
# # #     return {"model_call_count": current_counter + 1}


# # # # 创建智能体，设置middleware
# # # agent = create_agent(
# # #     model="deepseek-xxx", middleware=[retry_model], checkpointer=InMemorySaver()
# # # )
# # # config = {"configurable": {"thread_id": "1"}}

# # # # 调用智能体
# # # response = agent.invoke(
# # #     {
# # #         "messages": [HumanMessage("Hello")],
# # #     },
# # #     config,
# # # )

# # # print(response)


# # import time

# # from dotenv import load_dotenv
# # from langchain.agents import create_agent
# # from langchain.agents.middleware import wrap_tool_call
# # from langchain.tools import tool
# # from langchain_core.messages import ToolMessage
# # load_dotenv()

# # @tool
# # def divide(a: float, b: float) -> str:
# #     """计算 a 除以 b。"""
# #     return str(a / b)


# # @wrap_tool_call
# # def monitor_tool(request, handler):
# #     name = request.tool_call["name"]
# #     args = request.tool_call["args"]
# #     print(f"[调用前] {name} 参数={args}")

# #     start = time.time()
# #     try:
# #         result = handler(request)  # 真正执行工具
# #     except Exception as e:
# #         # 工具报错时不让整个 agent 崩溃，把错误作为结果返回给模型
# #         return ToolMessage(
# #             content=f"工具执行失败：{e}",
# #             tool_call_id=request.tool_call["id"],
# #         )

# #     print(f"[调用后] {name} 耗时 {time.time() - start:.3f}s")
# #     return result


# # agent = create_agent(
# #     model='deepseek-flash',  # 你已经创建好的模型对象
# #     tools=[divide],
# #     middleware=[monitor_tool],
# # )

# # response = agent.invoke({"messages": [{"role": "user", "content": "10 除以 0 等于几？"}]})
# # print(response)
# # for i in response['messages']:
# #     i.pretty_print()

# from typing import Any, Callable
# from dotenv import load_dotenv
# from langchain.tools import tool
# from langchain.agents import create_agent
# from langgraph.checkpoint.memory import InMemorySaver
# from langchain.messages import HumanMessage
# from langchain.agents.middleware import after_model
# from langchain.agents import AgentState
# from langgraph.runtime import Runtime
# from langchain.agents.middleware import wrap_model_call
# from langchain.agents.middleware import ModelRequest,ModelResponse
# from langchain.agents.middleware import wrap_model_call
# from collections.abc import Callable
# from pydantic.dataclasses import dataclass

# load_dotenv()
# # 定义一个context，记录用户是否开启思考模式
# @dataclass
# class UserContext:
#     thinking: bool = False


# @wrap_model_call
# def dynamic_model_settings(
#     request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
# ) -> ModelResponse:

#     # 获取上下文参数thinking，是否开启思考模式
#     thinking = request.runtime.context.thinking

#     # 如果Thinking为True，则开启思考模式，否则关闭思考模式
#     thinking_type = "enabled" if thinking else "disabled"
#     model_settings = {"extra_body": {"thinking": {"type": thinking_type}}}

#     # 覆盖request中的model参数
#     modified_request = request.override(model_settings=model_settings)
#     return handler(modified_request)


# # 创建智能体，设置middleware
# agent = create_agent(
#     model="deepseek-flash",
#     middleware=[dynamic_model_settings],
#     context_schema=UserContext,
# )

# # 调用智能体，并初始化state
# response = agent.invoke(
#     {"messages": [HumanMessage("Hello")]},
#     context=UserContext(thinking=True),  # 通过Context控制思考模式开关
# )

# print(response)


from typing import Any, Callable, NotRequired
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage,AIMessage
from langchain.agents.middleware import after_model
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from langchain.agents.middleware import wrap_model_call
from langchain.agents.middleware import ModelRequest,ModelResponse
from langchain.agents.middleware import wrap_model_call
from collections.abc import Callable
from pydantic.dataclasses import dataclass
from langchain.agents.middleware import AgentMiddleware,hook_config


load_dotenv()
# 1.定义自定义state，记录模型调用次数
class CustomAgentState(AgentState):
    """扩展Agent状态，添加自定义字段"""

    model_call_count: NotRequired[int]  # 模型调用次数


# 2.定义中间件
class ModelCallLimitMiddleware(AgentMiddleware[CustomAgentState]):

    def __init__(self, max_limit: int = 10):
        super().__init__()
        self.max_limit = max_limit

    # after_model hook，模型调用次数计数
    def after_model(
        self, state: CustomAgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        current_count = state.get("model_call_count", 0)
        return {"model_call_count": current_count + 1}

    # before_model hook，校验模型调用次数是否超限
    @hook_config(can_jump_to=["end"])
    def before_model(
        self, state: CustomAgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        # 获取模型调用次数
        current_count = state.get("model_call_count", 0) + 1
        # 判断是否超限
        print(f"当前模型调用次数：{current_count}/{self.max_limit}")
        if current_count > self.max_limit:
            return {
                "jump_to": "end",
                "messages": AIMessage(f"模型调用次数超过最大限制：{self.max_limit}！"),
            }
        return None


# @before_model(can_jump_to=["end"])
# def check_call_limit(state: CustomAgentState, runtime: Runtime) -> dict[str, Any] | None:
#     pass
# 创建智能体，设置middleware

agent = create_agent(
    model="deepseek-chat",
    middleware=[ModelCallLimitMiddleware(max_limit=2)],
    checkpointer=InMemorySaver(),
    state_schema=CustomAgentState,
)
config = {"configurable": {"thread_id": "1"}}

# 调用智能体，并初始化state
response = agent.invoke(
    {
        "messages": [HumanMessage("Hello")],
        "model_call_count": 0,
    },
    config,
)

print(response)
