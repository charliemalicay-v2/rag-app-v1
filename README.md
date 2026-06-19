# RAG App v1

A Retrieval-Augmented Generation (RAG) application that combines document retrieval with LLM-powered answer generation. The app loads documents from JSON files, stores them in a vector database, retrieves relevant documents for queries, and generates answers using either OpenAI's GPT or a local Ollama model. The project also exposes a FastAPI endpoint for query-based access.

## Features

- **Document Loading**: Load and process documents from JSON files
- **Vector Embeddings**: Use sentence-transformers for semantic search
- **Vector Database**: Chroma Cloud for storing and retrieving document embeddings
- **LLM Integration**: Support for both OpenAI GPT and local Ollama models
- **Duplicate Detection**: Automatic skipping of already-indexed documents
- **Semantic Search**: Retrieve top-k documents most relevant to queries

## Prerequisites

### System Requirements
- Python 3.8+
- Pipenv (for dependency management)
- 2GB+ free disk space

### External Dependencies & API Keys

#### 1. **Chroma Cloud** (Vector Database) - Required
- **Description**: Cloud-hosted vector database for storing and retrieving document embeddings
- **Setup Steps**:
  1. Sign up at [chroma.com](https://www.chroma.com)
  2. Create a new project/database in your Chroma Cloud dashboard
  3. Get your credentials:
     - API Key (`CHROMA_API_KEY`)
     - Tenant name (`CHROMA_TENANT`)
     - Database name (`CHROMA_DATABASE`)
  4. Add these to your `.env` file (see Configuration section)

#### 2. **OpenAI API Key** (Optional)
- **Description**: Used for GPT-4o-mini model responses. If not provided, the app falls back to local Ollama
- **Setup Steps**:
  1. Go to [platform.openai.com](https://platform.openai.com/account/api-keys)
  2. Create an API key
  3. Add `OPENAI_API_KEY=your_key_here` to `.env`
- **Cost**: Pay-as-you-go (check OpenAI pricing)

#### 3. **Ollama** (Optional - Local LLM Fallback)
- **Description**: Free, local language model for generating answers when OpenAI is not available
- **Setup Steps**:
  1. Download and install from [ollama.ai](https://ollama.ai)
  2. Start Ollama server:
     ```bash
     ollama serve
     ```
  3. Pull a model (in another terminal):
     ```bash
     ollama pull llama2
     # or for a smaller model:
     ollama pull llama2-mini
     ```
  4. Set in `.env`:
     ```
     OLLAMA_MODEL=llama2
     ```
- **Cost**: Free
- **Note**: The app communicates with Ollama via HTTP API (localhost:11434), so ensure Ollama is running before executing the pipeline

#### 4. **HuggingFace Token** (Optional)
- **Description**: For faster downloads of sentence-transformer models. Without it, you'll see a warning but it still works
- **Setup Steps**:
  1. Get token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
  2. Add `HF_TOKEN=your_token_here` to `.env`
- **Cost**: Free (requires account)

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Chroma Cloud (Required)
CHROMA_API_KEY=your_chroma_api_key
CHROMA_TENANT=your_tenant_name
CHROMA_DATABASE=your_database_name

# OpenAI (Optional - leave empty to use Ollama)
OPENAI_API_KEY=your_openai_key

# Ollama (Used if OPENAI_API_KEY is not set)
OLLAMA_MODEL=llama2
OLLAMA_PATH=/path/to/ollama  # Usually auto-detected

# HuggingFace (Optional)
HF_TOKEN=your_hf_token
```

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd rag-app-v1
   ```

2. **Install dependencies** using Pipenv:
   ```bash
   pipenv install
   ```
   This installs all required packages from the `Pipfile`

3. **Activate the virtual environment**:
   ```bash
   pipenv shell
   ```

## Running the Script

### Basic Execution

```bash
pipenv run python rag_pipeline.py
```

### In WSL/Ubuntu

```bash
wsl -d Ubuntu-26.04 -e bash -lc 'cd /mnt/c/Users/charl/Desktop/current_projects/github_projects/rag-app-v1 && pipenv run python rag_pipeline.py'
```

### Detailed Workflow

The script performs the following steps:

1. **Load Environment Variables**: Reads `.env` configuration
2. **Load Documents**: Reads all JSON files from the `datasets/` directory
3. **Add New Documents**: Uploads documents to Chroma Cloud (skips duplicates)
4. **Query Processing**: 
   - Converts sample query to embeddings
   - Retrieves top-2 most relevant documents from Chroma
   - Generates answer using OpenAI GPT or Ollama
5. **Output**: Prints results as JSON with query, retrieved documents, and answer

## Running the FastAPI Endpoint

### Start the API server

```bash
pipenv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Health check

```bash
curl http://localhost:8000/health
```

### Query endpoint

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a zero-day vulnerability?", "top_k": 2}'
```

### Example `/query` response

```json
{
  "query": "What is a zero-day vulnerability?",
  "retrieved_docs": [
    "A zero-day vulnerability is a software flaw that...",
    "Zero-day attacks exploit vulnerabilities before..."
  ],
  "answer": "A zero-day vulnerability is a previously unknown security flaw...",
  "distances": [0.2543, 0.3891]
}
```

### Example Output

```json
{
  "query": "What is a zero-day vulnerability?",
  "retrieved_docs": [
    "A zero-day vulnerability is a software flaw that...",
    "Zero-day attacks exploit vulnerabilities before..."
  ],
  "answer": "A zero-day vulnerability is a previously unknown security flaw...",
  "distances": [0.2543, 0.3891]
}
```

## Project Structure

```
rag-app-v1/
├── api.py                # FastAPI endpoint wrapper for the RAG pipeline
├── rag_pipeline.py       # Main RAG pipeline script
├── ingestion.py          # (Optional) Data ingestion utilities
├── Pipfile               # Dependency manifest
├── README.md             # This file
├── .env                  # Configuration (Git-ignored)
├── datasets/
│   ├── data_1.json       # Sample dataset
│   └── data_2.json       # Sample dataset
└── test-scripts/
    └── test_chroma.py    # Chroma connection test
```

## Troubleshooting

### "Missing OPENAI_API_KEY in .env"
- **Cause**: OpenAI key not set
- **Solution**: Either add your OpenAI API key to `.env`, or ensure Ollama is running for local LLM

### "Cannot connect to Ollama"
- **Cause**: Ollama server not running
- **Solution**: Start Ollama with `ollama serve` in another terminal

### "Chroma Cloud credentials missing"
- **Cause**: Missing `CHROMA_API_KEY`, `CHROMA_TENANT`, or `CHROMA_DATABASE`
- **Solution**: Verify these are correctly set in `.env`

### "No JSON files found in datasets/"
- **Cause**: `datasets/` directory is empty
- **Solution**: Add JSON files to the `datasets/` directory

## Vector Database: Chroma Cloud

**Why Chroma?**
- Cloud-hosted: No local setup required
- Scalable: Handles millions of documents
- Easy integration: Simple Python API
- Free tier available for testing

**Key Features Used:**
- `get_or_create_collection()`: Manages document collections
- `add()`: Stores documents with embeddings
- `query()`: Performs semantic search
- Automatic ID generation using MD5 hashes to prevent duplicates

**Alternative Vector Databases** (if you want to switch):
- Pinecone
- Weaviate
- Milvus
- Qdrant

## Performance Notes

The script has been optimized to use Ollama's HTTP API instead of subprocess calls for better performance in WSL environments.

## Dependencies

- `chromadb`: Vector database client
- `sentence-transformers`: Embedding generation
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests to Ollama
- `fastapi`: Web framework for serving the API
- `uvicorn`: ASGI server for running FastAPI

See `Pipfile` for complete dependency list.

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]