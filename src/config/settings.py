import os
from dotenv import load_dotenv

# Try to import streamlit for secrets (only works when running in Streamlit)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

load_dotenv()


class Settings():
    def __init__(self):
        # Try to get API key from multiple sources
        api_key = os.getenv("GROQ_API_KEY")
        
        # If not found and Streamlit is available, try Streamlit secrets
        if not api_key and STREAMLIT_AVAILABLE:
            try:
                if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
                    api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                pass  # Secrets might not be configured
        
        self.GROQ_API_KEY = api_key
        self.MODEL_NAME = "llama-3.1-8b-instant"
        self.TEMPERATURE = 0.9
        self.MAX_RETRIES = 3
    
    def validate_api_key(self):
        """Validate that GROQ_API_KEY is set"""
        if not self.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. Please set it as an environment variable "
                "or in a .env file. For Streamlit Cloud, add it in the app settings/secrets."
            )
        return True

settings = Settings()