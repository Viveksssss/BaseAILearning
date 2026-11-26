from langchain_text_splitters import MarkdownHeaderTextSplitter

with open(
    r"C:\Users\v1252\Desktop\RAG  LLM 工程高频面试题速记手册.md", "r", encoding="utf-8"
) as f:
    doc = f.read()

# 切分依据，这里是按照三级标题
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

# 创建切分器
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on, strip_headers=False  # 文本中是否携带标题
)

# 切分文档，接收str，返回值是list[Document]
chunks = markdown_splitter.split_text(doc)

for chunk in chunks:
    print(chunk.model_dump_json(indent=2))
