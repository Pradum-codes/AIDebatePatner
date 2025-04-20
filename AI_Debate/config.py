import google.generativeai as genai
import pyttsx3

# Set up Gemini API Key
API_KEY = "AIzaSyBhmtN74htSaKlDUVQ_LBXW29V4vTIWAKI"
genai.configure(api_key=API_KEY)

# Initialize Speech Engine
engine = pyttsx3.init()
