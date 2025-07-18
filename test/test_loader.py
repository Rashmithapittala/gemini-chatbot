import sys
import os

# Add the project root directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loader.url_loader import load_documents_from_urls

# Read URLs from file
with open("data/gitlab_links.txt") as f:
    urls = [line.strip() for line in f.readlines()]

# Load documents
docs = load_documents_from_urls(urls)

# Preview the first document's content
print(f"Loaded {len(docs)} documents.")
print(docs[0].page_content[:500])  
print(docs[1].page_content[:500]) 
