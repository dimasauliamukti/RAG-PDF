import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from text_cleaning import text_cleaning
from uuid import uuid4


def chunking(path):
    all_chunks = []

    for filename in os.listdir(path):
        if not filename.endswith(".pdf"):
            continue

        file = os.path.join(path, filename)

        loader = PyPDFLoader(file)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=80,
            separators=["\n\n", "\n", ".", " "]
        )

        # page_content and metadata
        docs = []
        for page in pages:
            text = text_cleaning(page.page_content)
            docs.append(Document(page_content=text, metadata=page.metadata))

        # print(docs)
        chunks = splitter.split_documents(docs)

        for idx, chunk in enumerate(chunks):
            page_number = chunk.metadata["page"]
            uid_chunk = f"{file}_page{page_number}_chunk{idx}_{uuid4().hex[:8]}"
            chunk.metadata["chunk_id"] = uid_chunk
        all_chunks.extend(chunks)

    return all_chunks
