# Development Test: RAG Pipeline Implementation

## 🎯 Objective

This test evaluates your ability to:

- ✅ Implement a simple Retrieval-Augmented Generation (RAG) pipeline
- ✅ Work with vector databases (FAISS, Chroma, Weaviate, Pinecone)
- ✅ Utilize text embeddings for document retrieval
- ✅ Integrate LLMs for context-aware responses

**⏱️ Estimated time:** ~60 minutes

---

## 📋 Task Overview

Build a basic RAG pipeline that:

1. **Ingest** text documents into a vector database
2. **Embed** documents using pre-trained models
3. **Retrieve** relevant documents based on user queries
4. **Generate** responses using an LLM with retrieved context

---

## ✨ Requirements

### Core Requirements

- **Language:** Python
- **Vector Database:** FAISS, ChromaDB, Weaviate, or Pinecone
- **LLM Provider:** OpenAI API (or alternative)
- **Documents:** Minimum 5 text documents
- **Retrieval Method:** Cosine similarity-based search

### Response Format

```json
{
  "query": "User question",
  "retrieved_docs": [
    "Document snippet 1",
    "Document snippet 2"
  ],
  "answer": "LLM-generated response"
}
```
---

## 📚 Starter Dataset

Index these **5 documents** in your vector database:

### Document 1: Cybersecurity Fundamentals
```
Cybersecurity is the practice of protecting systems and networks from attacks. 
It includes measures like firewalls, intrusion detection, and encryption.
```

### Document 2: Zero-Day Vulnerabilities
```
A zero-day vulnerability is an undisclosed flaw in software that attackers 
can exploit before the vendor issues a fix.
```

### Document 3: Two-Factor Authentication
```
Two-factor authentication (2FA) enhances security by requiring users to 
provide two forms of verification before gaining access.
```

### Document 4: Machine Learning Models
```
Machine learning models require large datasets and are often fine-tuned 
to improve accuracy for specific tasks.
```

### Document 5: CIA Triad
```
The CIA triad—Confidentiality, Integrity, and Availability—is a foundational 
concept in cybersecurity.
```

---

## 🚀 Task Instructions

### Step 1: Setup Environment

Install required dependencies:

```bash
pip install openai faiss-cpu sentence-transformers chromadb python-dotenv
```

### Step 2: Convert Documents into Embeddings

- Use a pre-trained embedding model (e.g., `all-MiniLM-L6-v2` from `sentence-transformers`)
- Store embeddings in your chosen vector database
- Generate unique IDs for each document

### Step 3: Implement a Retrieval Function

- Accept a user query as input
- Convert query to embedding using the same model
- Perform similarity search to find **top 2 most relevant documents**
- Return ranked results with relevance scores

### Step 4: Generate Response using LLM

- Pass retrieved documents as context to the LLM
- Include the user query
- Return structured JSON response with:
  - Original query
  - Retrieved document snippets
  - LLM-generated answer

---

## 📤 Expected Output

### Example Query
```
"What is a zero-day vulnerability?"
```

### Expected Response

```json
{
  "query": "What is a zero-day vulnerability?",
  "retrieved_docs": [
    "A zero-day vulnerability is an undisclosed flaw in software that attackers can exploit before the vendor issues a fix.",
    "Cybersecurity is the practice of protecting systems and networks from attacks."
  ],
  "answer": "A zero-day vulnerability refers to an unpatched software flaw that attackers can exploit before the software vendor issues a fix. It is a significant risk in cybersecurity because vendors have no time to develop and release patches."
}
```

---

## 🎁 Bonus Challenge (Optional)

If you finish early, consider:

- 🔌 **API Endpoint:** Expose the RAG pipeline as a REST API using FastAPI
- 💾 **Query Caching:** Implement caching for repeated queries to improve performance
- 📊 **Metrics:** Add logging for retrieval quality and response latency

---

## 📝 Submission Instructions

Submit the following:

### 1. Implementation
- **File:** `rag_pipeline.py`
- **Content:** Full RAG pipeline implementation with:
  - Document ingestion
  - Embedding generation
  - Retrieval logic
  - LLM integration

### 2. Documentation
- **File:** `README.md`
- **Include:**
  - Setup and installation steps
  - How to run the script
  - Required API keys and environment variables
  - Vector database choice and setup instructions
  - Example usage and sample output

### 3. Configuration
- **File:** `.env` (template: `.env.example`)
- **Include:** API keys and database credentials

---

## ⚡ Quick Reference

| Component | Choice |
|-----------|--------|
| Vector DB | ChromaDB (Cloud) |
| Embedding Model | `all-MiniLM-L6-v2` |
| LLM | OpenAI GPT-4 / Claude |
| Language | Python 3.8+ |
| Framework | FastAPI (optional) |

---

**Good luck! 🚀**
