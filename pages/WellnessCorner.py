import streamlit as st
import random

if 'user' not in st.session_state:
    st.warning("Please login first.")
    st.stop()
st.set_page_config(page_title="Motivating Visuals", layout="centered")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


motivating_data = {
    "Nature & Peace": [
        {
            "url": "https://images.pexels.com/photos/417173/pexels-photo-417173.jpeg",
            "caption": "Sunset over green hills",
            "quote": "Breathe in peace, breathe out stress."
        },
        {
            "url": "https://images.pexels.com/photos/624015/pexels-photo-624015.jpeg",
            "caption": "Ocean waves at sunrise",
            "quote": "You are the calm in your own storm."
        }
    ],
    "Happy People": [
        {
            "url": "https://images.pexels.com/photos/1704488/pexels-photo-1704488.jpeg",
            "caption": "Friends laughing together",
            "quote": "Joy shared is joy doubled."
        },
        {
            "url": "https://images.pexels.com/photos/708440/pexels-photo-708440.jpeg",
            "caption": "Joyful dance moment",
            "quote": "Let yourself feel the joy of now."
        }
    ],
    "Cute Animals": [
        {
            "url": "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg",
            "caption": "Golden retriever puppy smiling",
            "quote": "Sometimes a wagging tail is all you need."
        },
        {
            "url": "https://images.pexels.com/photos/747993/pexels-photo-747993.jpeg",
            "caption": "Kitten peeking out of a box",
            "quote": "A small moment of cuteness can change your day."
        }
    ],
    "Cozy & Calm": [
        {
            "url": "https://images.pexels.com/photos/374885/pexels-photo-374885.jpeg",
            "caption": "Cozy reading corner",
            "quote": "Find calm in the quiet corners of your life."
        },
        {
            "url": "https://images.pexels.com/photos/5566693/pexels-photo-5566693.jpeg",
            "caption": "Warm lights and a book",
            "quote": "Peace is often a warm light and a still heart."
        }
    ]
}

# -- UI Layout --
st.title("🌈 Feel-Good Space")
st.markdown("Select a mood below to lift your spirits with peaceful visuals and calming content.")

mood = st.selectbox("What do you feel like seeing?", list(motivating_data.keys()))

if st.button("✨ Inspire Me"):
    chosen = random.choice(motivating_data[mood])
    st.image(chosen["url"], caption=chosen["caption"],use_container_width=True)
    st.success(f" *{chosen['quote']}*")


with st.expander("🎥 Relax with a peaceful video"):
    st.video("https://www.youtube.com/embed/2OEL4P1Rz04")

with st.expander("🎧 Listen to calm background music"):
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# Sidebar logout button
with st.sidebar:
    #st.markdown("---")
    if st.button("Logout"):
        st.session_state.clear()
        st.success("Logged out successfully.")
        st.switch_page("Welcome.py")  # Redirect to login/signup page

