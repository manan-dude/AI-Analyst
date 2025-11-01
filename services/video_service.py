# app/services/video_service.py
import os
import uuid
import asyncio
from pathlib import Path
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from app.core.clients import gemini_client, whisper_model
from app.config import settings
from app.utils.logger import logger

try:
    import ffmpeg
except ImportError:
    ffmpeg = None

class VideoService:
    """Service for video analysis operations."""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def get_youtube_transcript(video_id: str) -> str:
        """Fetch transcript from YouTube."""
        logger.info(f"📹 Fetching transcript for video: {video_id}")
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([entry['text'] for entry in transcript_list])
            logger.info(f"✅ Transcript fetched: {len(transcript)} characters")
            return transcript
        except Exception as e:
            logger.error(f"❌ Failed to fetch transcript: {e}")
            raise
    
    @staticmethod
    async def extract_audio_from_video(video_path: str, audio_path: str) -> bool:
        """Extract audio from video file using FFmpeg."""
        if not ffmpeg:
            logger.error("❌ FFmpeg not installed")
            return False
        
        try:
            logger.info("🎵 Extracting audio with FFmpeg...")
            await asyncio.to_thread(
                ffmpeg.input(video_path)
                .output(audio_path, acodec='mp3', ac=1, ar='16000')
                .overwrite_output()
                .run,
                capture_stdout=True,
                capture_stderr=True
            )
            logger.info("✅ Audio extracted successfully")
            return True
        except Exception as e:
            logger.error(f"❌ FFmpeg extraction failed: {e}")
            return False
    
    @staticmethod
    async def transcribe_audio(audio_path: str) -> str:
        """Transcribe audio using Whisper."""
        if not whisper_model:
            raise Exception("Whisper model not initialized")
        
        logger.info("📝 Transcribing audio with Whisper...")
        try:
            segments, info = await asyncio.to_thread(
                whisper_model.transcribe,
                audio_path,
                beam_size=5
            )
            transcript = " ".join([segment.text for segment in segments])
            logger.info(f"✅ Transcription complete: {len(transcript)} characters")
            return transcript
        except Exception as e:
            logger.error(f"❌ Transcription failed: {e}")
            raise
    
    @staticmethod
    def analyze_transcript(transcript: str) -> dict:
        """Analyze transcript using Gemini."""
        logger.info("🤖 Analyzing transcript with Gemini...")
        
        analysis_prompt = f"""
You are an expert pitch analyst. Analyze the following video transcript from a pitch presentation.

TRANSCRIPT:
---
{transcript[:15000]}
---

Provide a comprehensive analysis in the following JSON format:

{{
    "video_title": "Extract or infer the pitch/company name",
    "duration": "Estimate duration from transcript",
    "channel": "Speaker/Company name if mentioned",
    "executive_summary": "2-3 sentence overview of the pitch",
    "key_insights": [
        "First major insight",
        "Second major insight",
        "Third major insight",
        "Fourth major insight",
        "Fifth major insight"
    ],
    "main_points": [
        "First main point from the pitch",
        "Second main point",
        "Third main point",
        "Fourth main point"
    ],
    "notable_slides": [
        {{
            "timestamp": "0:45",
            "description": "Problem statement slide - described the market gap"
        }},
        {{
            "timestamp": "2:30",
            "description": "Solution overview - demonstrated the product"
        }}
    ],
    "action_items": [
        "First recommendation or action item",
        "Second recommendation",
        "Third recommendation"
    ]
}}

Focus on business insights, problem-solution fit, market opportunity, competitive advantages, and traction indicators.
Output ONLY valid JSON, no markdown code blocks.
"""
        
        response = gemini_client.models.generate_content(
            model=settings.GENERATIVE_MODEL,
            contents=analysis_prompt,
        )
        
        # Parse JSON response
        raw_text = response.candidates.content.parts.text
        json_text = raw_text.strip()
        
        # Clean markdown
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]
        
        import json
        return json.loads(json_text.strip())

video_service = VideoService()
