from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
import google.generativeai as genai
from dotenv import load_dotenv
import os
#python -m spacy download en_core_web_sm

# Load API key from .env file
load_dotenv()
# Configure the Google Generative AI client with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Directory where the FAISS vector store is saved
VECTOR_STORE_DIR = "vectorstore/index"

# Pre-check for Vector Store
if not os.path.exists(VECTOR_STORE_DIR):
    print(f"Error: Vector store not found at {VECTOR_STORE_DIR}.")
    print("Please run 'python data_ingestion.py' first to build the GitLab knowledge base.")
    exit()

# Initialize the HuggingFaceEmbeddings model.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the FAISS vector store from the local directory.
# 'allow_dangerous_deserialization=True' is used as per your original code. ???????
db = FAISS.load_local(VECTOR_STORE_DIR, embeddings, allow_dangerous_deserialization=True)

# Create a retriever from the FAISS database.
retriever = db.as_retriever(search_kwargs={"k": 5})

# Initialize the Gemini model for generating responses.
model = genai.GenerativeModel("models/gemini-2.5-flash")

def ask(query: str, chat_history: list):
    docs = retriever.get_relevant_documents(query)
    relevant_docs = [doc for doc in docs if len(doc.page_content.strip()) > 200]
    context = ""
    prompt = ""

    if relevant_docs:
        context = "\n\n".join([doc.page_content for doc in relevant_docs[:3]])
        if query.lower() not in context.lower() and not any(q in context.lower() for q in query.lower().split()):
            print("Retrieved context doesn't match query. Falling back to general knowledge.")
            context = ""

    # Limit to last 5 interactions
    limited_history = chat_history[-10:]  # Since it's alternating HumanMessage and AIMessage

    # Build chat history string
    history_str = ""
    for msg in limited_history:
        if isinstance(msg, HumanMessage):
            history_str += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history_str += f"Bot: {msg.content}\n"

    # Final prompt
    if context:
        prompt = f"""{history_str}
Use the following context to answer the user's latest question. If the context does not help, rely on your general knowledge.

Context:
{context}

User: {query}
Answer:"""
    else:
        prompt = f"""{history_str}
Answer the following question using your general knowledge.

User: {query}
Answer:"""

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()

        generate_followups = len(query.split()) > 3 or "?" in query
        suggestions = []
        if generate_followups:
            followup_prompt = f"""List 2 helpful follow-up questions a user might ask based on this answer:\n\n{answer}\n\nFollow-up Questions:"""
            followup_resp = model.generate_content(followup_prompt)
            suggestions = [
                line.strip("-• ").strip()
                for line in followup_resp.text.strip().split("\n")
                if line.strip() and "follow-up" not in line.lower()
            ]
        return answer, suggestions[:2]
    except Exception as e:
        return f"An error occurred while generating response: {e}", []


if __name__ == "__main__":
    print("Gemini Chatbot (type 'exit' to quit)\n")
    chat_history = []

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            print("Exiting chatbot. Goodbye!")
            break
        if not query.strip():
            print("Bot: Please enter a valid question.")
            continue

    # Unpack the returned tuple
        answer, suggestions = ask(query, chat_history)
        print("\nBot:", answer)

    # Store only the answer in chat history
        chat_history.append(HumanMessage(content=query))
        chat_history.append(AIMessage(content=answer))

        if suggestions:
            print("\n Suggested Follow-ups:")
            for s in suggestions:
                print(f"- {s}")

