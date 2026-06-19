from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag_pipeline import answer_query

app = FastAPI(title='RAG App API', version='1.0')


class QueryRequest(BaseModel):
    query: str
    top_k: int = 2


@app.get('/health')
def health_check():
    return {'status': 'ok'}


@app.post('/query')
def query_endpoint(request: QueryRequest):
    try:
        result = answer_query(request.query, top_k=request.top_k)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
