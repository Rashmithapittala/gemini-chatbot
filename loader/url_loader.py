from langchain_community.document_loaders import UnstructuredURLLoader
from bs4 import BeautifulSoup
import requests

def extract_links_recursive(root_url, max_depth=2, visited=None):
    if visited is None:
        visited = set()
    if max_depth == 0 or root_url in visited:
        return []
    
    visited.add(root_url)
    try:
        res = requests.get(root_url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)
                 if a['href'].startswith("http") and "gitlab.com" in a['href']]
        
        all_links = [root_url]
        for link in links:
            all_links.extend(extract_links_recursive(link, max_depth - 1, visited))
        return list(set(all_links))
    except Exception as e:
        print(f"Failed to fetch {root_url}: {e}")
        return []

def load_documents_from_urls(urls):
    loader = UnstructuredURLLoader(urls=urls)
    return loader.load()
