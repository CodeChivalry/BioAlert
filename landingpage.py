import streamlit as st
from utils.firebase_auth import login_user, signup_user
st.set_page_config(page_title="BioAlert", layout="centered")

st.title("BioAlert: Real-Time Stress & Fatigue Monitoring")

st.markdown("""
BioAlert is a real-time dashboard that analyzes biosignal data like EEG, EDA, HR, and ACC to detect signs of stress and fatigue.  
It uses ML models trained on the MEFAR dataset, helping users monitor their mental wellness without external hardware.

### Features:
- Live stress & fatigue detection
- AI wellness chatbot support
- Secure login to your personal dashboard
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
    st.switch_page("pages/dashboard.py")