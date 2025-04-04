import streamlit as st
from utils.chatbot import get_gemini_reply

st.set_page_config(page_title="BioAlert Dashboard", layout="wide")

#  Block access if not logged in
if 'user' not in st.session_state:
    st.warning("Please login first.")
    st.stop()

# Welcome Message
st.title(f"📊 Welcome, {st.session_state['user'].split('@')[0].capitalize()}")
st.markdown("This is your **BioAlert** dashboard for monitoring stress & fatigue in real-time.")

#  Sidebar Chatbot
with st.sidebar:
    st.markdown("###  Chat with BioBuddy")
    st.caption("Your AI buddy for stress relief and support ")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    #  User input
    user_input = st.text_input(" Say something to BioBuddy", key="user_input")

    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append(("You", user_input))
            reply = get_gemini_reply(user_input)
            st.session_state.chat_history.append(("BioBuddy", reply))

    # Clear chat option
    if st.button("Clear Chat"):
        st.session_state.chat_history = []

    st.markdown("---")
    st.markdown("###  Conversation")

    # Safe display of history
    for chat in st.session_state.chat_history:
        if isinstance(chat, tuple) and len(chat) == 2:
            sender, msg = chat
            st.markdown(f"**{sender}**: {msg}")
        else:
            st.markdown(" Invalid message format")
