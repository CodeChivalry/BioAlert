import streamlit as st
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["stress-db"]
collection = db["sensor_data"]

st.title("📊 Recent Sensor Data Entries")

if st.checkbox("Show Recent Entries"):
    df = pd.DataFrame(list(collection.find().sort("timestamp", -1).limit(5)))
    if "_id" in df:
        df = df.drop(columns=["_id"])
    st.write(df)
