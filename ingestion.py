import os
import json
import hashlib
from pathlib import Path
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

# Load documents from all JSON files in datasets folder
documents = []
datasets_dir = Path('datasets')
json_files = sorted(datasets_dir.glob('*.json'))

if not json_files:
    print("No JSON files found in datasets folder.")
    exit()

print(f"Found {len(json_files)} JSON files in datasets folder:\n")

for json_file in json_files:
    with open(json_file, 'r') as f:
        file_docs = json.load(f)
        if isinstance(file_docs, list):
            documents.extend(file_docs)
            print(f"  ✓ Loaded {len(file_docs)} docs from {json_file.name}")
        else:
            print(f"  ✗ Skipped {json_file.name} - expected list, got {type(file_docs).__name__}")

print(f"\nTotal documents loaded: {len(documents)}\n")

# Generate unique IDs and filter out existing documents
new_docs = []
new_ids = []

for doc in documents:
    # Create unique ID based on document hash
    doc_id = hashlib.md5(doc.encode()).hexdigest()
    
    # Check if document already exists
    existing = collection.get(ids=[doc_id])
    
    if not existing['ids']:  # Document doesn't exist
        new_docs.append(doc)
        new_ids.append(doc_id)
        print(f"✓ Adding new document: {doc[:60]}...")
    else:
        print(f"⊘ Skipping existing document: {doc[:60]}...")

# Embed and add only new documents
if new_docs:
    embeddings = [model.encode(doc).tolist() for doc in new_docs]
    collection.add(
        ids=new_ids,
        documents=new_docs,
        embeddings=embeddings,
    )
    print(f"\n✓ Successfully added {len(new_docs)} new documents to collection.")
else:
    print(f"\n✓ No new documents to add. All {len(documents)} documents already exist.")

print(f"\nCollection now contains {collection.count()} total documents.")

query = "What can I use for local vector search?"
query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print(results)
# client.persist()
