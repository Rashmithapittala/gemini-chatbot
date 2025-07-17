import streamlit as st
from chatbot import ask  # Your ask() function
from langchain_core.messages import HumanMessage, AIMessage

# --- Page Config ---
st.set_page_config(page_title="GitLab Gemini Chatbot", layout="centered")
st.title("🤖 GitLab Gemini Chatbot")
st.markdown("Ask me anything about GitLab's Handbook and Direction pages!")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

# --- User Input ---
query = st.text_input(
    "Enter your question:",
    placeholder="e.g., What is GitLab's OKR policy?",
    key="input_query"
)

# --- Ask Button ---
if st.button("Ask") and query.strip():
    with st.spinner("Thinking..."):
        try:
            response, _ = ask(query, st.session_state.chat_history)

            # Update histories
            st.session_state.chat_history.extend([
                HumanMessage(content=query),
                AIMessage(content=response)
            ])
            st.session_state.chat_display.append((query, response))

        except Exception as e:
            error_msg = f"❌ Error: {e}"
            st.session_state.chat_display.append((query, error_msg))

# --- Display Chat History ---
if st.session_state.chat_display:
    st.subheader("📜 Chat History")
    for user_msg, bot_msg in reversed(st.session_state.chat_display):
        st.markdown(f"**🧑 You:** {user_msg}")
        st.markdown(f"**🤖 Bot:** {bot_msg}")
        st.markdown("---")
