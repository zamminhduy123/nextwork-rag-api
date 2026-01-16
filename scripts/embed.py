#💡 What does this script do?
# Reads k8s.txt and stores it in Chroma as embeddings (numerical representations) for semantic search. This prepares your knowledge base for the RAG system.

import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

with open("k8s.txt", "r") as f:
    text = f.read()

collection.add(documents=[text], ids=["k8s"])

print("Embedding stored in Chroma")
