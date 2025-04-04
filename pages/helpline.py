import streamlit as st
import googlemaps
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("YOUR_GOOGLE_MAPS_API_KEY")

if not GOOGLE_MAPS_API_KEY:
    st.error("Google Maps API key not found. Please check your .env file.")


gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY )

def get_coordinates(location_name):
    geocode_result = gmaps.geocode(location_name)
    if not geocode_result:
        return None
    loc = geocode_result[0]["geometry"]["location"]
    return (loc["lat"], loc["lng"])


def get_nearby_medical_stores(location_name):
    coords = get_coordinates(location_name)
    if not coords:
        return []

    places = gmaps.places_nearby(location=coords, radius=5000, type='pharmacy')
    return places.get("results", [])


def get_helpline_numbers():
    return {
        "India": "+91 9152987821",
        "USA": "988 (Mental Health Hotline)",
        "UK": "116 123 (Samaritans)"
    }

def show_helplines():
    st.title("📍 Seek Assistance Near You")
    
    location = st.text_input("Enter your location (City or Coordinates)")
    if st.button("Find Nearby Medical Stores"):
        if location:
            stores = get_nearby_medical_stores(location)
            for store in stores[:5]:
                st.write(f"🏥 {store['name']} - {store['vicinity']}")
        else:
            st.warning("Please enter a location.")
    
    country = st.selectbox("Select your country", list(get_helpline_numbers().keys()))
    st.write(f"📞 Helpline: {get_helpline_numbers()[country]}")

show_helplines()