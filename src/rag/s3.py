from langchain_ollama import OllamaEmbeddings
import numpy as np

ollamaEmbeddings = OllamaEmbeddings(
    model='qwen3-embedding:0.6b',
    dimensions=1024
)

text = "我爱死上班了"
vector1 = ollamaEmbeddings.embed_query(text)
vector2 = ollamaEmbeddings.embed_query("我不爱上班")

def cosin_similarity(vec1,vec2):
    dot = np.dot(vec1,vec2)
    return dot / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


print(cosin_similarity(vector1, vector2))
