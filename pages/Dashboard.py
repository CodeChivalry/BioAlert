import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from pymongo import MongoClient
import joblib
import os
from dotenv import load_dotenv

st.set_page_config(page_title="BioAlert Dashboard", layout="wide")

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI)
db = client["stress-db"]
collection = db["sensor_data"]

# Paths to Model & Scaler
model_path = "pages/stress_model.pkl"
scaler_path = "pages/scaler.pkl"

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

if 'user' not in st.session_state:
    st.warning("Please login first.")
    st.stop()

st.title(f"📊 Welcome, {st.session_state['user'].split('@')[0].capitalize()}")
st.markdown("This is your **BioAlert** dashboard for monitoring stress & fatigue in real-time.")


if st.button("Check Stress/Fatigue Level"):
    recent_entry = collection.find_one(sort=[("timestamp", -1)])

    if recent_entry:
        df = pd.DataFrame([recent_entry])
        df = df.drop(columns=["_id", "timestamp"], errors="ignore")
        df_scaled = scaler.transform(df)
        prediction = model.predict(df_scaled)[0]

        st.subheader("🧠 Prediction Result:")
        if prediction == 1:
            st.error("⚠️ High Stress/Fatigue Detected!")
        else:
            st.success("✅ Normal Stress/Fatigue Level")
    else:
        st.warning("⚠️ No data found in the database!")


@st.cache_data(ttl=5)
def fetch_latest_data():
    cursor = collection.find().sort("timestamp", -1).limit(100)
    df = pd.DataFrame(list(cursor))
    if not df.empty:
        df = df.drop(columns=["_id"], errors="ignore")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
    return df


def plot_signal(signal_names, title, y_label):
    df = fetch_latest_data()
    available_signals = [s for s in signal_names if s in df.columns]
    if available_signals:
        fig = px.line(df, x="timestamp", y=available_signals, 
                      title=title, labels={"timestamp": "Time", "value": y_label})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"⚠️ No data available for {title} yet!")


st.subheader("🧠 EEG (Brain Activity)")
plot_signal(["Theta", "Alpha1", "Alpha2", "Beta1", "Beta2", "Gamma1", "Gamma2", "Attention", "Meditation"], 
            "EEG (Brain Activity)", "EEG Signal")

st.subheader("❤️ BVP (Blood Volume Pulse)")
plot_signal(["BVP"], "BVP (Blood Volume Pulse)", "BVP Signal")

st.subheader("🔵 EDA (Electrodermal Activity)")
plot_signal(["EDA"], "EDA (Electrodermal Activity)", "EDA Signal")

st.subheader("💓 Heart Rate (BPM)")
plot_signal(["HR"], "Heart Rate (BPM)", "Heart Rate")

st.subheader("📡 Accelerometer Data")
plot_signal(["AccX", "AccY", "AccZ"], "Accelerometer (Movement Data)", "Acceleration")


st.query_params["refresh"] = str(time.time())

from utils.chatbot import get_gemini_reply

with st.sidebar:
    st.markdown("### 💬 Chat with BioBuddy")
    st.caption("Your AI buddy for stress relief and support")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Say something to BioBuddy", key="user_input")

    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append(("You", user_input))
            reply = get_gemini_reply(user_input)
            st.session_state.chat_history.append(("BioBuddy", reply))

    if st.button("Clear Chat"):
        st.session_state.chat_history = []

    st.markdown("---")
    st.markdown("### 🗨️ Conversation History")

    for chat in st.session_state.chat_history:
        if isinstance(chat, tuple) and len(chat) == 2:
            sender, msg = chat
            st.markdown(f"**{sender}**: {msg}")
        else:
            st.markdown("⚠️ Invalid message format")
