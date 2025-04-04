import streamlit as st

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard", "Chatbot", "Database"])

# ✅ Use correct lowercase folder name
if page == "Home":
    st.switch_page("pages/home.py")  
elif page == "Dashboard":
    st.switch_page("pages/dashboard.py")
elif page == "Chatbot":
    st.switch_page("pages/chatbot.py")
elif page == "Database":
    st.switch_page("pages/recent_entries.py")
