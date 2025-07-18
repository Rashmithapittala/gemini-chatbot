import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loader.url_loader import extract_links_recursive, load_documents_from_urls
from processor.text_splitter import split_documents
from embedder.embed_and_store import embed_and_save

if __name__ == "__main__":
    root_urls = [
        "https://about.gitlab.com/handbook/",
        "https://about.gitlab.com/direction/"
    ]

    all_urls = set()

    print("Extracting GitLab links...")
    for root_url in root_urls:
        urls = extract_links_recursive(root_url, max_depth=2)
        print(f"Found {len(urls)} URLs from {root_url}")
        all_urls.update(urls)

    print(f"Total unique URLs collected: {len(all_urls)}")

    print("Loading documents...")
    documents = load_documents_from_urls(list(all_urls))

    print("Splitting documents...")
    chunks = split_documents(documents)

    print("Embedding and saving to FAISS...")
    embed_and_save(chunks)

    print("Data ingestion completed.")
