import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# =====================================
# LOAD DOCUMENTS
# =====================================

documents = []

DOC_FOLDER = "D:\Sound\iit\Week15_assgmnt\Technology_Rag_asst\Documents"

for filename in os.listdir(DOC_FOLDER):

    if filename.endswith(".txt"):

        path = os.path.join(DOC_FOLDER, filename)

        loader = TextLoader(
            path,
            encoding="utf-8"
        )

        documents.extend(loader.load())

print(f"Loaded {len(documents)} documents")


# =====================================
# SPLIT INTO CHUNKS
# =====================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# =====================================
# EMBEDDINGS
# =====================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# =====================================
# CREATE FAISS INDEX
# =====================================

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

vectorstore.save_local("faiss_index")

print("FAISS index saved successfully")