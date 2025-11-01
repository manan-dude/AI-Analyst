# app/core/clients.py
from google import genai
import chromadb
from app.config import settings
from app.utils.logger import logger

# Initialize Gemini client
logger.info("🚀 Initializing Gemini client...")
gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
logger.info("✅ Gemini client initialized")

# Initialize ChromaDB
logger.info(f"💾 Setting up ChromaDB at: {settings.CHROMA_DB_PATH}")
chroma_client = chromadb.PersistentClient(path=str(settings.CHROMA_DB_PATH))
logger.info("✅ ChromaDB client initialized")

# Initialize Whisper model (optional)
whisper_model = None
try:
    from faster_whisper import WhisperModel
    whisper_model = WhisperModel(
        settings.WHISPER_MODEL,
        device=settings.WHISPER_DEVICE,
        compute_type=settings.WHISPER_COMPUTE_TYPE
    )
    logger.info("✅ Whisper model initialized")
except ImportError:
    logger.warning("⚠️ Whisper not installed. Video upload disabled.")
except Exception as e:
    logger.warning(f"⚠️ Whisper initialization failed: {e}")
