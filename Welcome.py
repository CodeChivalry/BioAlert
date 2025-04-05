import streamlit as st
from utils.firebase_auth import login_user, signup_user
st.set_page_config(page_title="BioAlert", layout="centered")

# Load the custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



st.image("assets/welcome_banner.png",use_container_width=True)





st.markdown("""
BioAlert is a wellness platform that analyzes  biosignals like EEG, EDA, BVP, and ACC to detect signs of **stress and fatigue** using a machine learning model trained on the MEFAR dataset. 

It provides a secure, interactive dashboard designed to support mental/physical well-being and offers a range of features to help users manage their health effectively.

### Key Features:
- Fatigue detection using biosignals
- AI-powered chatbot for mental wellness support
- Helpline numbers based on your location
- A safe space with calming music and uplifting video content
- Firebase-secured login & session handling
""")

st.divider()
st.subheader("Login / Signup")

choice = st.selectbox("Choose", ["Login", "Signup"])
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if choice == "Login":
    if st.button("Login"):
        if email and password:
            response = login_user(email, password)
            if response["status"] == "success":
                st.success("Logged in successfully.")
                st.session_state["logged_in"] = True
                st.session_state["user"] = email
                st.rerun()  
            else:
                st.error(response["message"])
        else:
            st.warning("Please fill in all fields.")
else:
    if st.button("Signup"):
        if email and password:
            response = signup_user(email, password)
            if response["status"] == "success":
                st.success("Account created. Please login.")
            else:
                st.error(response["message"])
        else:
            st.warning("Please fill in all fields.")


if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.switch_page("pages/Dashboard.py")