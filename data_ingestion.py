# data_ingestion.py
import sys
import os

# Make sure the parent dir (Gemini-Chatbot/) is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loader.url_loader import extract_links_recursive, load_documents_from_urls
from processor.text_splitter import split_documents
from embedder.embed_and_store import embed_and_save

if __name__ == "__main__":
    print("🔍 Extracting GitLab links...")
    root_url = "https://about.gitlab.com/handbook/"
    urls = extract_links_recursive(root_url, max_depth=2)
    print(f"🌐 Found {len(urls)} URLs.")

    print("📄 Loading documents...")
    documents = load_documents_from_urls(urls)

    print("✂️ Splitting documents...")
    chunks = split_documents(documents)

    print("💾 Embedding and saving to FAISS...")
    embed_and_save(chunks)

    print("✅ Data ingestion completed.")
