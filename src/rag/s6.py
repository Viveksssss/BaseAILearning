"""
带"危险操作需用户确认"的 agent 完整示例（LangChain 1.x + LangGraph）

依赖: pip install langchain langgraph  （再装你所用模型的集成包，如 langchain-openai / langchain-ollama）
运行: python confirm_demo.py
然后输入类似: 帮我删除 build 目录
"""

import re
import shlex
import uuid

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

# ============ 1. 模型（按你的实际情况修改这一行）============
# OpenAI:  "openai:gpt-4o"
# Ollama:  "ollama:qwen3:8b"   （需要 pip install langchain-ollama）
load_dotenv()
model = init_chat_model("deepseek-flash")


# ============ 2. 工具：这里只是"模拟执行"，不会真的删文件 ============
@tool
def bash(command: str) -> str:
    """执行一条 shell 命令，返回输出。"""
    # 想真的执行，可换成:
    # import subprocess
    # r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
    # return r.stdout + r.stderr
    return f"[模拟执行成功] {command}"


# ============ 3. 判断命令是否危险（演示级别，规则很简单）============
DANGEROUS = {"rm", "rmdir", "mv", "dd", "mkfs", "shutdown", "chmod", "chown", "sudo"}


def is_dangerous(cmd: str) -> bool:
    # 按 ; && || | 拆成多个子命令，逐个看第一个单词
    for part in re.split(r"&&|\|\||;|\|", cmd):
        try:
            tokens = shlex.split(part)
        except ValueError:
            return True  # 解析失败，保守处理为危险
        if not tokens:
            continue
        if tokens[0] in DANGEROUS:
            return True
        if tokens[0] == "find" and ("-delete" in tokens or "-exec" in tokens):
            return True
    return False


# ============ 4. 中间件：危险命令 -> 暂停，等用户确认 ============
@wrap_tool_call
def guard(request, handler):
    call = request.tool_call
    cmd = call["args"].get("command", "")

    if call["name"] == "bash" and is_dangerous(cmd):
        # 注意：interrupt 之前不要放有副作用的代码，恢复时这段会重新执行一遍
        decision = interrupt({"command": cmd})  # <- 在这里暂停，值会传给调用方

        if decision != "approve":
            # 拒绝：把原因告诉模型，让它换方案
            return ToolMessage(
                content=f"用户拒绝执行该命令。原因/说明：{decision}",
                tool_call_id=call["id"],
            )

    return handler(request)  # 安全命令，或用户已批准 -> 真正执行工具


# ============ 5. 创建 agent（必须有 checkpointer，否则无法暂停恢复）============
agent = create_agent(
    model=model,
    tools=[bash],
    middleware=[guard],
    checkpointer=InMemorySaver(),
    system_prompt="你是一个命令行助手，需要操作文件时调用 bash 工具。每次只调用一个工具。",
)


# ============ 6. 主循环：处理用户输入 + 处理确认 ============
def main():
    config = {
        "configurable": {"thread_id": str(uuid.uuid4())}
    }  # 同一个 thread_id = 同一场对话

    while True:
        text = input("\n你> ").strip()
        if text in ("exit", "quit", ""):
            break

        result = agent.invoke({"messages": [HumanMessage(text)]}, config)

        # 只要结果里带 __interrupt__，说明 agent 暂停了，在等用户确认
        while "__interrupt__" in result:
            print(result['__interrupt__'])
            info = result["__interrupt__"][0].value
            print(f"\n⚠️  agent 想执行危险命令: {info['command']}")
            ans = input("允许吗？ y=允许 / n=拒绝 / 或直接输入拒绝理由 > ").strip()

            decision = "approve" if ans.lower() in ("y", "yes") else (ans or "n")

            # 用 Command(resume=...) 恢复，decision 会成为 interrupt() 的返回值
            result = agent.invoke(Command(resume=decision), config)

        print("\nAI>", result["messages"][-1].content)


if __name__ == "__main__":
    main()
