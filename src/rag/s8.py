from pymilvus import AnnSearchRequest, MilvusClient, WeightedRanker,RRFRanker
from langchain_ollama import OllamaEmbeddings
from sentence_transformers import CrossEncoder


ranker_weight = WeightedRanker(0.5, 0.5)
ranker_rrf = RRFRanker(60)
reranker = CrossEncoder("BAAI/bge-reranker-base", device="cpu")

embeddings = OllamaEmbeddings(
    model="qwen3-embedding:0.6b",  # 性价比高的模型
    dimensions=1024,  # 可选：减少维度以节省存储
)

COLLECTION_NAME = "rag_knowledge"
DIMENSION = 1024


client = MilvusClient("./resources/demo.db")  # 传本地路径，自动启动 Lite，没有则创建
client.load_collection(COLLECTION_NAME)

def hybrid_search(query: str, ranker,recall_k=3) -> list[list[dict[str, str]]]:
    # 1.创建稠密，稀疏请求

    query_embedding = embeddings.embed_query(query)

    dense_request = AnnSearchRequest(
        data=[query_embedding], anns_field="dense", param={}, limit=3
    )

    sparse_request = AnnSearchRequest(
        data=[query],
        anns_field="sparse",
        param={},
        limit=3,
    )

    reqs = [dense_request, sparse_request]
    res = client.hybrid_search(
        collection_name=COLLECTION_NAME,
        reqs=reqs,
        ranker=ranker,
        limit=recall_k,
        output_fields=["content", "h2"],
    )

    hits = res[0]
    texts = [h['entity']['content']for h in hits]
    scores = reranker.predict([(query, t) for t in texts])
    ranked = sorted(zip(hits, scores), key=lambda x: x[1], reverse=True)
    return [(h["entity"]["content"], float(s)) for h, s in ranked[:3]]

    docs = []
    for hits in res:
        document = []
        for hit in hits:
            document.append(
                {"content": hit["content"], "h2": hit["h2"], "score": hit["distance"]}
            )
        docs.append(document)

    return docs

# res = hybrid_search("描述一下我的经历", ranker_rrf)
# for outer in res :
#     for inner in outer:
#         print(f'相关性:{inner['score']}')
#         print(f'内容:{inner['content']}')
#     print('*'*50)


res = hybrid_search('描述一下此人的经历',ranker_rrf,2)
for text, score in res:
    print(f"{score:.4f}  {text}")
    print('*'*50)