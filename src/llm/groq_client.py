from langchain_groq import ChatGroq
from src.config.settings import settings


def groq_client_llm():
    """Initialize and return Groq LLM client with validation"""
    # Validate API key before creating client
    settings.validate_api_key()
    
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE
    )