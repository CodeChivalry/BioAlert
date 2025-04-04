import pyrebase
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

#  Firebase Config from .env
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
}

#  Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# ---------------------------
#  Sign Up Function
# ---------------------------
def signup_user(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return {"status": "success", "user": user}
    except Exception as e:
        print("Signup error:", e)
        error_msg = parse_firebase_error(e)
        return {"status": "error", "message": error_msg}

# ---------------------------
#  Login Function
# ---------------------------
def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return {"status": "success", "user": user}
    except Exception as e:
        print("Login error:", e)
        error_msg = parse_firebase_error(e)
        return {"status": "error", "message": error_msg}

# ---------------------------
# Firebase Error Parser
# ---------------------------
def parse_firebase_error(exception):
    try:
        error_str = str(exception)
        if "EMAIL_NOT_FOUND" in error_str:
            return "Email not found."
        elif "INVALID_PASSWORD" in error_str or "INVALID_EMAIL" in error_str:
            return "Invalid email or password."
        elif "EMAIL_EXISTS" in error_str:
            return "Email already in use."
        elif "WEAK_PASSWORD" in error_str:
            return "Password should be at least 6 characters."
        else:
            return error_str
    except Exception as e:
        return f"Unexpected error: {str(e)}"
