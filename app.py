import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
MONGO_URI = ""
client = MongoClient(MONGO_URI)
db = client["stress-db"]  # you can change this name
collection = db["sensor_data"]

st.title("🧠 Real-time Stress Input Form")

st.write("Enter sensor data below (based on MEFAR dataset):")

# All input fields from the CSV
time = st.text_input("Time (e.g. 2023-04-01 12:00:00)")
hr = st.number_input("Heart Rate (HR)", min_value=0.0)
hrv = st.number_input("Heart Rate Variability (HRV)", min_value=0.0)
rr = st.number_input("Respiration Rate (RR)", min_value=0.0)
bvp = st.number_input("Blood Volume Pulse (BVP)", min_value=0.0)
gsr = st.number_input("Galvanic Skin Response (GSR)", min_value=0.0)
temp = st.number_input("Temperature (TEMP)", min_value=0.0)
ibi = st.number_input("Interbeat Interval (IBI)", min_value=0.0)
scl = st.number_input("Skin Conductance Level (SCL)", min_value=0.0)
scr = st.number_input("Skin Conductance Response (SCR)", min_value=0.0)

if st.button("Submit"):
    entry = {
        "time": time,
        "HR": hr,
        "HRV": hrv,
        "RR": rr,
        "BVP": bvp,
        "GSR": gsr,
        "TEMP": temp,
        "IBI": ibi,
        "SCL": scl,
        "SCR": scr
    }
    collection.insert_one(entry)
    st.success("✅ Data saved to MongoDB!")




# Optional: Display recent entries
if st.checkbox("Show Recent Entries"):
    import pandas as pd
    df = pd.DataFrame(list(collection.find().sort("timestamp", -1).limit(5)))
    if "_id" in df:
        df = df.drop(columns=["_id"])
    st.write(df)
