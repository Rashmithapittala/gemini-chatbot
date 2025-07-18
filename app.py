import streamlit as st
from chatbot import ask  # Your ask() function
from langchain_core.messages import HumanMessage, AIMessage

# --- Page Config ---
st.set_page_config(page_title="GitLab Gemini Chatbot", layout="centered")
st.title("GitLab Gemini Chatbot")
st.markdown("Ask me anything about GitLab's Handbook and Direction pages!")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

if "temp_query" not in st.session_state:
    st.session_state.temp_query = ""

# --- Handle Ask ---
def handle_query():
    query = st.session_state.temp_query.strip()
    if not query:
        return

    with st.spinner("Thinking..."):
        try:
            response, suggestions = ask(query, st.session_state.chat_history)

            st.session_state.chat_history.extend([
                HumanMessage(content=query),
                AIMessage(content=response)
            ])
            st.session_state.chat_display.append((query, response, suggestions))
        except Exception as e:
            error_msg = f"Error: {e}"
            st.session_state.chat_display.append((query, error_msg, []))

    # Clear input box
    st.session_state.temp_query = ""

# --- User Input + Button ---
st.text_input(
    "Enter your question:",
    placeholder="e.g., What is GitLab's OKR policy?",
    key="temp_query",
    on_change=handle_query
)

# --- Display Chat History ---
# --- Display Chat History ---
if st.session_state.chat_display:
    st.markdown("### Chat History")
    for user_msg, bot_msg, suggestions in reversed(st.session_state.chat_display):
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Bot:** {bot_msg}")
        
        # Only show suggestions if available and non-empty
        if suggestions and any(s.strip() for s in suggestions):
            st.markdown("**Suggested Follow-ups:**")
            for s in suggestions:
                st.markdown(f"- {s}")
        
        st.markdown("---")

