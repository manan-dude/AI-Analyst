# app/api/routes/video_pitch.py
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models.request_models import VideoPitchRequest
from app.services.video_service import video_service
from app.config import settings
from app.utils.logger import logger

router = APIRouter(prefix="/api/video-pitch", tags=["Video Pitch"])

@router.post("/analyze")
async def analyze_youtube_video(request: VideoPitchRequest):
    """Analyze YouTube video pitch."""
    logger.info("="*70)
    logger.info("🎬 YOUTUBE VIDEO ANALYSIS REQUEST")
    
    try:
        # Extract video ID
        video_id = video_service.extract_video_id(request.youtube_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Get transcript
        transcript = video_service.get_youtube_transcript(video_id)
        
        # Analyze transcript
        analysis_data = video_service.analyze_transcript(transcript)
        analysis_data['youtube_url'] = request.youtube_url
        
        logger.info("✅ YouTube video analysis completed")
        return JSONResponse(content={"success": True, "data": analysis_data})
        
    except Exception as e:
        logger.error(f"❌ YouTube analysis failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@router.post("/upload")
async def analyze_uploaded_video(file: UploadFile = File(...)):
    """Analyze uploaded video file."""
    logger.info("="*70)
    logger.info("📤 VIDEO UPLOAD ANALYSIS REQUEST")
    
    file_id = str(uuid.uuid4())
    video_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.mp4")
    audio_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.mp3")
    
    try:
        # Save video
        with open(video_path, "wb") as f:
            f.write(await file.read())
        
        # Extract audio
        if not await video_service.extract_audio_from_video(video_path, audio_path):
            raise Exception("Failed to extract audio from video")
        
        # Transcribe
        transcript = await video_service.transcribe_audio(audio_path)
        
        # Analyze
        analysis_data = video_service.analyze_transcript(transcript)
        analysis_data['filename'] = file.filename
        
        logger.info("✅ Video upload analysis completed")
        return JSONResponse(content={"success": True, "data": analysis_data})
        
    except Exception as e:
        logger.error(f"❌ Video upload failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    finally:
        # Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
