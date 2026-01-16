"""Configuration module for the AI Agent application."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration (not required for local models)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "not_required")
    
    # Vector Database Configuration
    chroma_persist_directory: str = os.getenv(
        "CHROMA_PERSIST_DIRECTORY", 
        "./data/chroma_db"
    )
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # Application Settings
    debug_mode: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Model Settings (local models)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chat_model: str = "local-simple-llm"
    temperature: float = 0.7
    max_tokens: int = 500
    
    # RAG Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
