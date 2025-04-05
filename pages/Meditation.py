import streamlit as st
import time
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Guided Meditation", layout="centered")

# State to track duration and start trigger
if "meditation_duration" not in st.session_state:
    st.session_state.meditation_duration = None
if "session_started" not in st.session_state:
    st.session_state.session_started = False

st.title("🧘 Guided Meditation")
st.markdown("Choose how long you'd like to meditate and follow the animation to relax.")

# Duration selection
if not st.session_state.session_started:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🕐 1 Minute"):
            st.session_state.meditation_duration = 60
            st.session_state.session_started = True
            st.rerun()
    with col2:
        if st.button("🕒 3 Minutes"):
            st.session_state.meditation_duration = 180
            st.session_state.session_started = True
            st.rerun()
    with col3:
        if st.button("🕔 5 Minutes"):
            st.session_state.meditation_duration = 300
            st.session_state.session_started = True
            st.rerun()

# Only show this once a session starts
if st.session_state.session_started:

    st.subheader(f"⏳ Meditation in progress ({st.session_state.meditation_duration//60} min)")
    st.markdown("Focus on your breath and let your thoughts flow.")

    # Breathing animation
    components.html("""
    <html>
    <head>
    <style>
    .circle {
      margin: 80px auto;
      width: 100px;
      height: 100px;
      border-radius: 50%;
      background-color: #88c9bf;
      animation: breathe 8s ease-in-out infinite;
    }
    @keyframes breathe {
      0%, 100% {
        transform: scale(1);
        opacity: 0.7;
      }
      50% {
        transform: scale(2.5);
        opacity: 1;
      }
    }
    </style>
    </head>
    <body>
      <div class="circle"></div>
    </body>
    </html>
    """, height=280)
    # Calm music (autoplay loop, hidden)
    with open("pages/calm_music.mp3", "rb") as f:
        encoded_audio = base64.b64encode(f.read()).decode()
    components.html(f"""
    <div style="margin:0; padding:0;">
    <audio autoplay loop hidden>
        <source src="data:audio/mp3;base64,{encoded_audio}" type="audio/mp3">
    </audio>
    </div>
    """, height=0)

    # Timer
    with st.spinner("Take this time for yourself..."):
        time.sleep(st.session_state.meditation_duration)

    # Completion message
    st.success("✅ Well done! You've completed your meditation.")
    if st.button("🔁 Start Again"):
        st.session_state.meditation_duration = None
        st.session_state.session_started = False
        st.rerun()
