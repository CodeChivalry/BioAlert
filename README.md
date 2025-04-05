# BioAlert: Biosignal-Based Fatigue and Stress Detection Dashboard

**BioAlert** is a wellness platform that analyzes biosignals like EEG, EDA, BVP, and ACC to detect signs of stress and fatigue using a machine learning model trained on the MEFAR dataset.
## Features

- 📊 **Real-time Stress Detection:** ML-based prediction from the latest biosignal data entry.
- 💬 **AI Wellness Chatbot:** AI-powered chatbot for emotional support and stress management.
- 🎈 **Feel-Good Space:** Generates happy images, videos, and audios on-demand to uplift your mood.
- 🧘 **Meditation Corner:** Calming audio-based and guided meditations to help you relax.
- 🆘 **Helpline Page:** Shows nearby medical stores and provides quick access to mental health helplines using Google Maps API.

---

## 🔍 Website Walkthrough

1. **Dashboard:** View your latest stress prediction and trends.
2. **Input Form** Add a new user entry for BioSignal data based on EEG, EDA, BVP, and ACC
3. **Chatbot:** Chat with an AI-based assistant for emotional guidance.
4. **Meditation Corner:** Access meditation sessions to calm your mind.
5. **Feel-Good Space:** Get a dose of happiness via uplifting multimedia.
6. **Helpline & Medical Stores:** Locate nearby pharmacies and helplines with a click.

---

## 🛠️ Local Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- [Streamlit](https://streamlit.io/)
- Gemini API Key (for chatbot)
- Google Maps API Key(for helpline/medical store locator)
- Firebase

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/BioAlert.git
cd BioAlert
```
### 2. Set Virtual Environment
```bash
python -m venv venv
```

Activate the Virtual Environment
**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Set Environment Variables

Set up your API keys in a .env file
- Firebase API Keys for Authentication and database
- GEMINI_API_KEY
- GOOGLE_MAPS_API_KEY


### 5. Run the Application

```bash
streamlit run app.py
```
