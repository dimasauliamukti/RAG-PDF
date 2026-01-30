def retrieve(query, vectorstore, k=5):
    return vectorstore.similarity_search(query, k=k)
