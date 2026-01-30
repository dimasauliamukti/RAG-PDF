from embeddings import embed
from preprocess import chunking
from config import VECTOR_DIR, DOCUMENTS

chunk = chunking(DOCUMENTS)
vdatabase = embed(chunk, VECTOR_DIR)
print("Success Uploading")
