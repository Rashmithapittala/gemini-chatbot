# Gemini-Powered GitLab Chatbot

This is a Gemini-based chatbot with RAG to answer questions from GitLab's Handbook and Direction pages. It uses LangChain, FAISS, and Streamlit to create an interactive chat experience on top of scraped and chunked documentation.

---

## Features

- Crawls and extracts content from GitLab Handbook and Direction pages  
- Chunks and embeds content using SentenceTransformer  
- Stores embeddings in a FAISS vector index  
- Uses Gemini Pro for answer generation with relevant document context  
- Clean Streamlit-based UI with support for follow-up prompts and chat history (up to 5 turns)

---

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/your-username/gemini-gitlab-chatbot.git
cd gemini-gitlab-chatbot

### 2. Clone the Repository

python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up Environment Variables

Create a .env file in the root directory and add your Gemini API key:

GOOGLE_API_KEY=your_google_gemini_api_key

## Build the index

python data_ingestion.py 

## Run the streamlit app

streamlit run app.py