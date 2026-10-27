from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama

# =====================================
# LOAD EMBEDDING MODEL
# =====================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# =====================================
# LOAD FAISS INDEX
# =====================================

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# =====================================
# LOAD MISTRAL
# =====================================

llm = ChatOllama(
    model="mistral"
)

# =====================================
# MEMORY
# =====================================

chat_history = []

print("\nTechnology Support Assistant Ready")
print("Type 'exit' to quit\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    You are a Technology Support Assistant.

    Use ONLY the retrieved context.

    Rules:
    1. Answer only from the retrieved context.
    2. Use conversation history for follow-up questions.
    3. Never use outside knowledge.
    4. If the answer is not clearly found in the context, respond exactly:

    I don't have enough information in the provided documents.

    Conversation History:
    {chat_history}

    Retrieved Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)

    answer = response.content.strip()

    if "I don't have enough information" in answer:
        answer = "I don't have enough information in the provided documents."

    chat_history.append(
        f"User: {question}\nAssistant: {answer}"
    )

    print("\nBot:", answer)
    print()