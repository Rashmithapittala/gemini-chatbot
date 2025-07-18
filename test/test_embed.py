import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loader.url_loader import load_documents_from_urls
from processor.text_splitter import split_documents
from embedder.embed_and_store import embed_and_save

with open("data/gitlab_links.txt") as f:
    urls = [line.strip() for line in f.readlines()]

docs = load_documents_from_urls(urls)
chunks = split_documents(docs)
embed_and_save(chunks)
