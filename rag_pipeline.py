import os
import json
import hashlib
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')
OLLAMA_PATH = os.getenv('OLLAMA_PATH', '/mnt/c/Users/charl/AppData/Local/Programs/Ollama/ollama.exe')
CHROMA_API_KEY = os.getenv('CHROMA_API_KEY')
CHROMA_TENANT = os.getenv('CHROMA_TENANT')
CHROMA_DATABASE = os.getenv('CHROMA_DATABASE')

if not OPENAI_API_KEY:
    print('WARNING: Missing OPENAI_API_KEY in .env.')
    print('Falling back to Ollama local model if available.')
    print('Suggestion: install Ollama and use a free local model such as `llama2` or `llama2-mini`.')
    print('Set OLLAMA_MODEL in .env if you want a different local model.')
    print('Set OLLAMA_PATH in .env if your Ollama executable path differs.')

if not CHROMA_API_KEY or not CHROMA_TENANT or not CHROMA_DATABASE:
    raise ValueError('Missing Chroma Cloud credentials in .env')

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.CloudClient(api_key=CHROMA_API_KEY, tenant=CHROMA_TENANT, database=CHROMA_DATABASE)
collection = client.get_or_create_collection('documents')


def load_documents_from_datasets(dataset_path='datasets'):
    documents = []
    dataset_dir = Path(dataset_path)
    json_files = sorted(dataset_dir.glob('*.json'))

    if not json_files:
        raise FileNotFoundError(f'No JSON files found in {dataset_path}')

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            file_docs = json.load(f)
            if isinstance(file_docs, list):
                documents.extend(file_docs)
            # else:
            #     print(f'Skipped {json_file.name}: expected list, got {type(file_docs).__name__}')

    return documents


def add_documents_if_new(documents):
    new_docs = []
    new_ids = []

    for doc in documents:
        doc_id = hashlib.md5(doc.encode('utf-8')).hexdigest()
        existing = collection.get(ids=[doc_id])
        if not existing['ids']:
            new_docs.append(doc)
            new_ids.append(doc_id)
        else:
            print(f'Skipping existing document: {doc[:60]}...')

    if new_docs:
        embeddings = [model.encode(doc).tolist() for doc in new_docs]
        collection.add(ids=new_ids, documents=new_docs, embeddings=embeddings)
        print(f'Added {len(new_docs)} new documents to the collection.')
    else:
        print('No new documents to add.')


def retrieve_top_docs(query, top_k=2):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=['documents', 'distances']
    )

    documents = results['documents'][0] if results['documents'] else []
    distances = results['distances'][0] if results['distances'] else []
    return documents, distances


def generate_answer(query, retrieved_docs):
    context = '\n\n'.join(f'- {doc}' for doc in retrieved_docs)
    prompt = (
        'Use the following documents to answer the query as accurately as possible. '
        'If the answer is not contained in the documents, say that the information is unavailable.\n\n'
        f'Context:\n{context}\n\n'
        f'Question: {query}\n\n'
        'Answer:'
    )

    if OPENAI_API_KEY:
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt},
            ],
            max_tokens=200,
            temperature=0.2,
        )
        return response.choices[0].message['content'].strip()

    # Fall back to Ollama local model
    ollama_prompt = {
        'model': OLLAMA_MODEL,
        'prompt': prompt,
        'temperature': 0.2,
        'max_tokens': 200,
    }

    try:
        proc = subprocess.run(
            [OLLAMA_PATH, 'run', OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            check=True,
        )
        output_text = proc.stdout.strip()
        if not output_text:
            raise RuntimeError('Ollama returned no output.')
        return output_text
    except FileNotFoundError:
        raise RuntimeError(
            f'Ollama executable not found at {OLLAMA_PATH}. Verify the path or install Ollama and retry.'
        )
    except subprocess.CalledProcessError as exc:
        stderr_text = exc.stderr.strip()
        raise RuntimeError(
            f'Ollama call failed: {stderr_text or exc.stdout.strip()}'
        )


def answer_query(query, top_k=2):
    retrieved_docs, distances = retrieve_top_docs(query, top_k=top_k)
    answer = generate_answer(query, retrieved_docs)
    return {
        'query': query,
        'retrieved_docs': retrieved_docs,
        'answer': answer,
        'distances': distances,
    }


if __name__ == '__main__':
    docs = load_documents_from_datasets('datasets')
    print(f'Loaded {len(docs)} documents from datasets.')
    add_documents_if_new(docs)

    sample_query = 'What is a zero-day vulnerability?'
    output = answer_query(sample_query, top_k=2)

    print(json.dumps(output, indent=2, ensure_ascii=False))
