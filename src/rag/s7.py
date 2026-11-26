# import turtle

# def curca(t,n,nivel):
#     if nivel == 0:
#         t.forward(n)
#     else:
#         curca(t,n/3,nivel - 1)
#         t.left(60)
#         curca(t,n/3,nivel - 1)
#         t.right(120)
#         curca(t,n/3,nivel-1)
#         t.left(60)
#         curca(t,n/3,nivel-1)

# t = turtle.Turtle()
# for i in range(4):
#     curca(t,300,3)
#     t.right(90)
# turtle.done()


from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from pymilvus import DataType, Function, FunctionType, MilvusClient


def prepare_docs():
    # =============1.准备文档================
    with open(
        r"C:\Users\v1252\Desktop\RAG  LLM 工程高频面试题速记手册.md",
        "r",
        encoding="utf-8",
    ) as f:
        doc = f.read()

    # =============2.切分文档================
    # 切分依据，这里是按照三级标题
    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
    ]

    # 创建切分器
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on, strip_headers=False  # 在正文中是否去除标题，False，不去除
    )

    # 切分文档, 返回的是 list[Document]
    docs = markdown_splitter.split_text(doc)

    return docs


docs = prepare_docs()


embeddings = OllamaEmbeddings(
    model="qwen3-embedding:0.6b",  # 性价比高的模型
    dimensions=1024,  # 可选：减少维度以节省存储
)


COLLECTION_NAME = "rag_knowledge"
DIMENSION = 1024


client = MilvusClient("./resources/demo.db")  # 传本地路径，自动启动 Lite，没有则创建


def create_collection():
    # 1.schema
    schema = client.create_schema(
        auto_id=False,  # 不自动生成id
        enable_dynamic_field=False,  # 是否允许动态字段
    )

    # 1.1.主键字段
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    # 1.2.稠密向量字段
    schema.add_field(field_name="dense", datatype=DataType.FLOAT_VECTOR, dim=1024)
    # 1.3.稀疏向量字段
    schema.add_field(field_name="sparse", datatype=DataType.SPARSE_FLOAT_VECTOR)
    # 1.4.普通元数据字段，用来做数据过滤
    schema.add_field(field_name="h2", datatype=DataType.VARCHAR, max_length=128)
    # 1.5.原始文档内容，需要被向量化
    schema.add_field(
        field_name="content",
        datatype=DataType.VARCHAR,
        max_length=2048,
        enable_analyzer=True,  # 允许对该字段分词，转BM25稀疏向量
        analyzer_params={"type": "jieba"},  # 指定分词方式，这里选择中文分词
    )
    # 1.6.添加BM25函数，可以自动把原始文档转BM25向量存储
    bm25_function = Function(
        name="text_bm25_emb",  # Function name
        input_field_names=["content"],  # 包含原始文档数据的字段的名称
        output_field_names=["sparse"],  # 稀疏向量字段的名称
        function_type=FunctionType.BM25,  # Set to `BM25`
    )
    schema.add_function(bm25_function)
    # 1.7.添加Embedding函数，可以自动把原始文档转稠密向量存储
    # text_embedding_function = Function(
    #     name="ali",  # Embedding函数的名称
    #     function_type=FunctionType.TEXTEMBEDDING,  # 函数类型，选择embedding function
    #     input_field_names=["content"],  # 用来转稠密向量的原始文本字段的名称
    #     output_field_names=["dense"],  # 存储稠密向量字段的名称
    #     params={  # 向量模型提供者的相关参数
    #         "provider": "openai",  # 模型提供者名称，例如"dashscope"
    #         "model_name": "qwen3-embedding:0.6b",  # 向量模型名称
    #     },
    # )
    # 将配置好的Embedding函数添加到现有的Schema中
    # schema.add_function(text_embedding_function)
    # 2.索引
    index_params = client.prepare_index_params()
    # 2.1.稠密向量索引
    index_params.add_index(
        field_name="dense",  # 字段名
        index_type="AUTOINDEX",  # 稠密向量索引方式
        metric_type="COSINE",  # 相似度计算方式，COSINE、IP
    )
    # 2.2.稀疏向量索引
    index_params.add_index(
        field_name="sparse",  # 字段名
        index_type="SPARSE_INVERTED_INDEX",  # 稀疏向量，采用倒排索引
        metric_type="BM25",  # 相似度计算方式，支持 BM25、IP
    )
    # 2.3.普通字段索引
    # index_params.add_index(field_name="h2", index_type="AUTOINDEX")

    # 3.创建collection
    client.create_collection(
        collection_name=COLLECTION_NAME, schema=schema, index_params=index_params
    )


if not client.has_collection(COLLECTION_NAME):
    create_collection()


def insert_docs(docs, batch_size=4):
    total = len(docs)

    for start in range(0, total, batch_size):
        batch_docs = docs[start : start + batch_size]
        texts = [doc.page_content for doc in batch_docs]

        print(f"正在处理：{start + 1} - {min(start + batch_size, total)} / {total}")

        # 1. 分批生成向量
        vectors = embeddings.embed_documents(texts)

        # 2. 组装数据
        data = []

        for i, (doc, vector) in enumerate(zip(batch_docs, vectors)):
            data.append(
                {
                    "id": start + i,
                    "h2": doc.metadata.get("h2", ""),
                    "content": doc.page_content,
                    "dense": vector,
                }
            )

        # 3. 分批写入 Milvus
        client.insert(collection_name=COLLECTION_NAME, data=data)

    print(f"全部完成，共写入 {total} 条数据")


# insert_docs(docs, batch_size=4)

# 将 Collection 加载到内存，准备进行检索
client.load_collection(collection_name=COLLECTION_NAME)


def search_docs(query, top_k=3):
    # 1. 将用户问题转换为向量
    query_vector = embeddings.embed_query(query)

    # 2. 在 Milvus 中进行相似度检索
    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[query_vector],
        limit=top_k,
        anns_field="dense",
        output_fields=["content", "h2"],
    )

    # 3. 提取检索结果
    documents = []

    for hits in results:
        ddcos = []
        for hit in hits:
            ddcos.append(
                {
                    "id": hit["id"],
                    "score": hit["distance"],
                    "text": hit["entity"]["content"],
                }
            )
        documents.append(ddcos)

    return documents


# 测试
query = "项目讲了什么"

results = search_docs(query, top_k=3)
for result in results:
    for item in result:
        print(f"相似度：{item['score']}")
        print(f"内容：{item['text']}")
        print("-" * 50)
    print('*'*100)
