from langchain_ollama.chat_models import ChatOllama

chat = ChatOllama(model="llama3", temperature=0.0)


def query(query, chunks):
    context_text = "\n\n".join([chunk.page_content for chunk in chunks])
    system_prompt = """You are a Retrieval-Augmented Generation (RAG) assistant.

    Rules:
    - Answer ONLY using facts stated in the provided context.
    - Do NOT infer, guess, or add external knowledge.
    - Do NOT merge information unless explicitly connected in the context.
    - If the answer is missing, incomplete, or unclear, respond exactly with:
    "I don't know based on the provided context."
    """

    user_prompt = f"""Context: {context_text}

    Question: {query}"""

    messages = [("system", system_prompt), ("user", user_prompt)]

    response = chat.invoke(messages)

    # Ambil content dari response
    return response.content  # ← tambahkan .content
