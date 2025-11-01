# app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # API Configuration
    API_TITLE: str = "AI Analyst Platform API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered startup analysis platform"
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    EMBEDDING_MODEL: str = 'models/text-embedding-004'
    GENERATIVE_MODEL: str = 'gemini-2.5-flash'
    
    # Storage Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    CHROMA_DB_PATH: Path = BASE_DIR / "chroma_db"
    LOG_FILE: Path = BASE_DIR / "app.log"
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]  # In production, specify exact origins
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: set = {'.pdf', '.mp4', '.mov', '.avi'}
    
    # Processing Settings
    MAX_PAGES_PDF: int = 10
    MAX_PAGES_RAG: int = 5
    CHUNK_SIZE: int = 1500
    CHUNK_OVERLAP: int = 300
    
    # Whisper Model Settings
    WHISPER_MODEL: str = "base"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_COMPUTE_TYPE: str = "int8"
    
    def __init__(self):
        """Create necessary directories on init."""
        self.UPLOAD_DIR.mkdir(exist_ok=True)
        self.CHROMA_DB_PATH.mkdir(exist_ok=True)
        
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

settings = Settings()
