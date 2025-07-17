import sys
import os

# Make sure the parent dir (Gemini-Chatbot/) is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loader.url_loader import load_documents_from_urls
from processor.text_splitter import split_documents

# Load URLs
with open("data/gitlab_links.txt") as f:
    urls = [line.strip() for line in f.readlines()]

# Load raw documents
docs = load_documents_from_urls(urls)

# Split into smaller chunks
chunks = split_documents(docs)

print(f"Split into {len(chunks)} chunks.")
print(len(chunks[0].page_content))
print(len(chunks[1].page_content))
print(len(chunks[2].page_content))
print(chunks[0].page_content[:1000])  # Preview one chunk
