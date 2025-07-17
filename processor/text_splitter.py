
from langchain.text_splitter import SpacyTextSplitter

def split_documents(docs, chunk_size=500, overlap=50):
    splitter = SpacyTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = splitter.split_documents(docs)
    total_tokens = sum(len(chunk.page_content) for chunk in chunks)
    print(f"✅ Split into {len(chunks)} chunks with ~{total_tokens} total characters")
    return chunks
#spacy optimises diff mean over chunk size
