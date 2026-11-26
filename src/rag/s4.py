from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_postgres.vectorstores import PGVector

with open(r'C:\Users\v1252\Desktop\RAG  LLM 工程高频面试题速记手册.md','r', encoding='utf-8') as f:
    doc = f.read()

headers_to_split_on = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),

]


markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on, strip_headers=False  # 在正文中是否去除标题，False，不去除
)


docs = markdown_splitter.split_text(doc)

for i, doc in enumerate(docs, start=1):
    doc.id = f"doc_{i}"


ollama_embeddings = OllamaEmbeddings(
    model="qwen3-embedding:0.6b",  # 性价比高的模型
    dimensions=1024,  # 可选：减少维度以节省存储
)

connection = "postgresql+psycopg://vivek:38324@localhost:5432/pg_db"

vector_store = PGVector(
    embeddings=ollama_embeddings,
    collection_name="rag_db",
    connection=connection,   
    use_jsonb=True,
)


ids = vector_store.add_documents(docs)
print(ids)


query = "描述你的主要经历"

# 相似度检索，返回值是list[Document]
results = vector_store.similarity_search(
    query=query,
    k=5,
)

# 打印结果
for doc in results:
    print(doc.model_dump_json(indent=2))
