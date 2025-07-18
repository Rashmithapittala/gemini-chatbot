from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import pickle

def embed_and_save(chunks, faiss_path="vectorstore/index"):
    # 1. Load embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 2. Convert chunks to vector store
    db = FAISS.from_documents(chunks, embeddings)

    # 3. Save vectorstore to disk
    if not os.path.exists("vectorstore"):
        os.makedirs("vectorstore")
    db.save_local(faiss_path)

    print(f"FAISS vector store saved to: {faiss_path}")
