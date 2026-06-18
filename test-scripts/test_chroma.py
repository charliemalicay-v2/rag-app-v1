import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

client = chromadb.CloudClient(
  api_key=os.getenv('CHROMA_API_KEY'),
  tenant=os.getenv('CHROMA_TENANT'),
  database=os.getenv('CHROMA_DATABASE')
)

model = SentenceTransformer("all-MiniLM-L6-v2")

collection = client.get_or_create_collection("documents")

documents = [
    "Chroma is a free local vector database.",
    "This is another document to store.",
    "Use it for RAG search and retrieval."
]

embeddings = [model.encode(doc).tolist() for doc in documents]

collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=documents,
    embeddings=embeddings,
)

query = "What can I use for local vector search?"
query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print(results)
# client.persist()
