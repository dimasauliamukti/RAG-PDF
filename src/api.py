from fastapi import FastAPI
from pydantic import BaseModel
from langchain_qdrant import QdrantVectorStore
from retrieval import retrieve
from user_query import query
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import VECTOR_DIR

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="RAG",
    path=VECTOR_DIR,  # path ke database lokal yang sudah ada
)


api = FastAPI()


# API
class QueryRequest(BaseModel):
    question: str


@api.post("/ask")
def RAG(req: QueryRequest):
    retri = retrieve(req.question, vector_db)
    rag = query(req.question, retri)
    return {"answer": rag}
