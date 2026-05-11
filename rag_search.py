from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "docs.index"
)

with open("docs.pkl", "rb") as f:

    chunks = pickle.load(f)


def search_docs(query, k=3):

    query_embedding = model.encode([query])

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    D, I = index.search(
        query_embedding,
        k
    )

    results = []

    for idx in I[0]:

        results.append(
            chunks[idx]
        )

    return "\n\n".join(results)