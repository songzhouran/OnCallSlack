from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chunks = []

docs_dir = "docs"

for filename in os.listdir(docs_dir):

    path = os.path.join(
        docs_dir,
        filename
    )

    if not os.path.isfile(path):
        continue

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

        parts = text.split("\n\n")

        for part in parts:

            part = part.strip()

            if len(part) < 20:
                continue

            chunks.append(part)

print("chunks:", len(chunks))

embeddings = model.encode(chunks)

embeddings = np.array(
    embeddings,
    dtype="float32"
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    "docs.index"
)

with open("docs.pkl", "wb") as f:

    pickle.dump(chunks, f)

print("RAG index built")