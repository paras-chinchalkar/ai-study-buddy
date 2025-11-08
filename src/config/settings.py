import os
from dotenv import load_dotenv

load_dotenv()


class Settings():
    def __init__(self):
        self.MODEL_NAME = "llama-3.1-8b-instant"
        self.TEMPERATURE = 0.9
        self.MAX_RETRIES = 3
        self._api_key = None
    
    @property
    def GROQ_API_KEY(self):
        """Get API key from multiple sources with lazy loading"""
        if self._api_key is not None:
            return self._api_key
        
        # First try environment variable
        api_key = os.getenv("GROQ_API_KEY")
        
        # If not found, try Streamlit secrets (only when Streamlit is available)
        if not api_key:
            try:
                import streamlit as st
                if hasattr(st, 'secrets'):
                    try:
                        # Try to access secrets - this works in Streamlit Cloud
                        if 'GROQ_API_KEY' in st.secrets:
                            api_key = st.secrets["GROQ_API_KEY"]
                    except (AttributeError, KeyError, TypeError):
                        # Secrets might not be configured or accessible yet
                        pass
            except ImportError:
                # Streamlit not available (e.g., during testing)
                pass
        
        # Cache the result
        self._api_key = api_key
        return api_key
    
    def validate_api_key(self):
        """Validate that GROQ_API_KEY is set"""
        if not self.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. Please set it as an environment variable "
                "or in a .env file. For Streamlit Cloud, add it in the app settings/secrets."
            )
        return True

settings = Settings()