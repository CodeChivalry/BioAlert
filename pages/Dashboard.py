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
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["stress-db"]
collection = db["sensor_data"]

model_path = "pages/stress_model.pkl"
scaler_path = "pages/scaler.pkl"

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

if 'user' not in st.session_state:
    st.warning("Please login first.")
    st.stop()

st.title(f"📊 Welcome, {st.session_state['user'].split('@')[0].capitalize()}")
st.markdown("This is your **BioAlert** dashboard for monitoring stress & fatigue in real-time.")

@st.cache_data(ttl=5)
def fetch_latest_data():
    cursor = collection.find().sort("timestamp", -1).limit(100)
    df = pd.DataFrame(list(cursor))
    if not df.empty:
        df = df.drop(columns=["_id"], errors="ignore")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
    return df

def plot_feedback_vs_prediction_over_time():
    df = fetch_latest_data()

    # Check for user feedback availability
    if "self_reported_stress" not in df.columns or df.empty:
        st.warning("No feedback data available to plot.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp")

    features = df.drop(columns=["timestamp", "self_reported_stress"], errors="ignore")
    df["ModelPrediction"] = model.predict_proba(scaler.transform(features))[:, 1]
    df.rename(columns={"self_reported_stress": "UserFeedback"}, inplace=True)

    fig = px.line(
        df,
        x="timestamp",
        y=["UserFeedback", "ModelPrediction"],
        labels={"value": "Stress Level", "timestamp": "Time", "variable": "Source"},
        title="User Feedback vs Model Prediction Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_signal(signal_names, title, y_label):
    df = fetch_latest_data()
    available_signals = [s for s in signal_names if s in df.columns]
    if available_signals:
        fig = px.line(df, x="timestamp", y=available_signals, 
                      title=title, labels={"timestamp": "Time", "value": y_label})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data available for {title} yet!")

if st.button("Check Stress/Fatigue Level"):
    recent_entry = collection.find_one(sort=[("timestamp", -1)])

    if recent_entry:
        df = pd.DataFrame([recent_entry])
        self_stress = df.get("self_reported_stress", pd.Series([None])).values[0]
        df = df.drop(columns=["_id", "timestamp", "self_reported_stress"], errors="ignore")
        df_scaled = scaler.transform(df)
        proba = model.predict_proba(df_scaled)
        confidence = proba[0][1]

        st.subheader("🧠 Prediction Result:")
        if confidence >= 0.5:
            st.error(f"⚠️ You are {confidence * 100:.2f}% likely to be stressed!")
        else:
            st.success(f"✅ You're probably okay! Only {confidence * 100:.2f}% chance of stress.")

        st.subheader("📈 Stress Feedback vs Model Prediction Over Time")
        plot_feedback_vs_prediction_over_time()
    else:
        st.warning("No data found in the database!")

# SIGNAL VISUALIZATIONS
st.subheader("EEG (Brain Activity)")
plot_signal(["Theta", "Alpha1", "Alpha2", "Beta1", "Beta2", "Gamma1", "Gamma2", "Attention", "Meditation"], 
            "EEG (Brain Activity)", "EEG Signal")

st.subheader("BVP (Blood Volume Pulse)")
plot_signal(["BVP"], "BVP (Blood Volume Pulse)", "BVP Signal")

st.subheader("EDA (Electrodermal Activity)")
plot_signal(["EDA"], "EDA (Electrodermal Activity)", "EDA Signal")

st.subheader("Heart Rate (BPM)")
plot_signal(["HR"], "Heart Rate (BPM)", "Heart Rate")

st.subheader("Accelerometer Data")
plot_signal(["AccX", "AccY", "AccZ"], "Accelerometer (Movement Data)", "Acceleration")

st.query_params["refresh"] = str(time.time())

# CHATBOT SIDEBAR
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

    if st.button("Logout"):
        st.session_state.clear()
        st.success("Logged out successfully.")
        st.switch_page("Welcome.py")

