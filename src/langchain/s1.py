import base64
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
load_dotenv()


@tool
def getWeather(location: str) -> str:
    '''
        Get weather of location
        Args:
            location:city name
    '''
    return f"Current location is {location}"


model = ChatDeepSeek(
    model="deepseek-flash",  # 或 deepseek-reasoner
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
print("🚀 正在调用大模型...")
with open(r"E:\Code\python\base\code.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")
response = model.stream([
        SystemMessage("你是一个助手，解答问题"),
        HumanMessage(content=[
            {
                "type":"text",
                "text":'这张图片是什么'
            },
            # {
            #     "type":"image_url",
            #     "image_url":{
            #         "url":f"data:image/jpg;base64,{image_b64}"
            #     }
            # }
            {
                "type":"image",
                "base64":image_b64,
                "mime_type":"image/jpg"
            }
        ])
])

# 5.打印结果
is_content = False
for chunk in response:
    rc = chunk.additional_kwargs.get('reasoning_content')
    if rc:
        print(f"\033[90m{rc}\033[0m", end="")
    elif chunk.content:
        if is_content is False:
            print()
            is_content = True
        print(chunk.content,end='')