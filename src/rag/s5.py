from langchain.agents.middleware import dynamic_prompt, ModelRequest,wrap_model_call,before_model
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()


connection = "postgresql+psycopg://vivek:38324@localhost:5432/pg_db"

ollama_embeddings = OllamaEmbeddings(
    model="qwen3-embedding:0.6b",  # 性价比高的模型
    dimensions=1024,  # 可选：减少维度以节省存储
)

vector_store = PGVector(
    embeddings=ollama_embeddings,
    collection_name="rag_db",
    connection=connection,
    use_jsonb=True,
)

@tool
def search_knowledge(query:str) -> str:
    """检索知识库，注意目前知识库只有个人简历相关的内容。"""
    docs = vector_store.similarity_search(query,k=2)
    return '\n\n'.join(d.page_content for d in docs)

@wrap_model_call
def rag_inject(request:ModelRequest,handler):
    msgs = request.messages
    user_input = msgs[-1].text
    
    docs = vector_store.similarity_search(user_input,k=2)
    context = '\n\n'.join(d.page_content for d in docs)
    
    new_msgs = HumanMessage(f'参考资料:\n{context}\n\n问题:{user_input}')
    
    
    # 模型调用
    response =  handler(request.override(messages=[*msgs[:-1],new_msgs]))

    # 调用后
    print()
    
    
    return response

# # 0.定义动态提示词中间件
# @dynamic_prompt
# def rag_prompt(request: ModelRequest):
#     # 1.拿到用户问题，也就是消息列表中的最后一条消息
#     user_input = request.state["messages"][-1].text

#     # 2.检索知识片段, list[Document], 拼接为字符串
#     docs = vector_store.similarity_search(user_input, k=2)
#     context = "\n\n".join(doc.page_content for doc in docs)

#     # 3.拼接新系统提示词
#     return f"""
#     你根据上下文回答用户问题，不能自己编造答案。答案要简短，直接引用原文。
#     Context: {context}
#     """


# 1.初始化模型
model = init_chat_model(
    "deepseek-v4-flash", 
    extra_body={"thinking": {"type": "disabled"}},
    
)

# 2.定义Agent
agent = create_agent(
    model,
    tools=[search_knowledge],
    # middleware=[rag_inject],
    system_prompt='当你调用工具的时候，请在最后的回复使用[]包裹给出基本的信息'
)


from langchain.messages import HumanMessage

# 测试
response = agent.invoke({"messages": [HumanMessage("此人经历如何？")]})
print("==============AI Message================")
print(response["messages"][-1].text)
