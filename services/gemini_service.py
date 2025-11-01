# app/services/gemini_service.py
import json
from typing import List
from app.core.clients import gemini_client
from app.config import settings
from app.utils.logger import logger

class GeminiService:
    """Service for interacting with Gemini API."""
    
    @staticmethod
    def generate_content(prompt: str, config: dict = None) -> str:
        """Generate content using Gemini."""
        try:
            response = gemini_client.models.generate_content(
                model=settings.GENERATIVE_MODEL,
                contents=prompt,
                config=config or {}
            )
            return response.text
        except Exception as e:
            logger.error(f"❌ Gemini generation failed: {e}")
            raise
    
    @staticmethod
    def generate_embeddings(texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        logger.info(f"🔢 Generating embeddings for {len(texts)} texts...")
        try:
            response = gemini_client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=texts
            )
            embeddings = [item.values for item in response.embeddings]
            logger.info(f"✅ Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"❌ Embedding generation failed: {e}")
            raise
    
    @staticmethod
    def parse_json_response(response_text: str) -> dict:
        """Parse JSON from Gemini response."""
        json_text = response_text.strip()
        
        # Remove markdown formatting
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]
        
        return json.loads(json_text.strip())

gemini_service = GeminiService()
