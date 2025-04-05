import streamlit as st
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if 'user' not in st.session_state:
    st.warning("Please login first.")
    st.stop()


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI)
db = client["stress-db"]  
collection = db["sensor_data"]

st.title(" Real-time Stress Input Form")

st.write("Enter sensor data below (based on MEFAR dataset):")

time = st.text_input("Time (e.g. 2023-04-01 12:00:00)")
bvp = st.number_input("Blood Volume Pulse (BVP)", format="%.15f", value=0.0)
eda = st.number_input("Electrodermal Activity (EDA)", format="%.15f", value=0.0)
temp = st.number_input("Temperature (TEMP)", format="%.15f", value=0.0)
acc_x = st.number_input("Accelerometer X (AccX)", format="%.15f", value=0.0)
acc_y = st.number_input("Accelerometer Y (AccY)", format="%.15f", value=0.0)
acc_z = st.number_input("Accelerometer Z (AccZ)", format="%.15f", value=0.0)
hr = st.number_input("Heart Rate (HR)", format="%.15f", value=0.0)
delta = st.number_input("EEG Delta", format="%.15f", value=0.0)
theta = st.number_input("EEG Theta", format="%.15f", value=0.0)
alpha1 = st.number_input("EEG Alpha1", format="%.15f", value=0.0)
alpha2 = st.number_input("EEG Alpha2", format="%.15f", value=0.0)
beta1 = st.number_input("EEG Beta1", format="%.15f", value=0.0)
beta2 = st.number_input("EEG Beta2", format="%.15f", value=0.0)
gamma1 = st.number_input("EEG Gamma1", format="%.15f", value=0.0)
gamma2 = st.number_input("EEG Gamma2", format="%.15f", value=0.0)
attention = st.number_input("Attention", format="%.15f", value=0.0)
meditation = st.number_input("Meditation", format="%.15f", value=0.0)
if st.button("Submit"):
    entry = {
        "BVP": bvp,
        "EDA": eda,
        "TEMP": temp,
        "AccX": acc_x,
        "AccY": acc_y,
        "AccZ": acc_z,
        "HR": hr,
        "Delta": delta,
        "Theta": theta,
        "Alpha1": alpha1,
        "Alpha2": alpha2,
        "Beta1": beta1,
        "Beta2": beta2,
        "Gamma1": gamma1,
        "Gamma2": gamma2,
        "Attention": attention,
        "Meditation": meditation,
        "timestamp": datetime.datetime.now()
    }
    collection.insert_one(entry)
    st.success("✅ Data saved to MongoDB!")

if st.checkbox("Show Recent Entries"):
    import pandas as pd
    df = pd.DataFrame(list(collection.find().sort("timestamp", -1).limit(5)))
    if "_id" in df:
        df = df.drop(columns=["_id"])
    st.write(df)

# Sidebar logout button
with st.sidebar:
    #st.markdown("---")
    if st.button("Logout"):
        st.session_state.clear()
        st.success("Logged out successfully.")
        st.switch_page("Welcome.py")  # Redirect to login/signup page

