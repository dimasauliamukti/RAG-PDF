from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


def embed(docs, path):
    qdrant = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        path=str(path),
        collection_name="RAG"
    )

    qdrant.client.close()

    return qdrant
