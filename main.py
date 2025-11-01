# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.config import settings
from app.utils.logger import logger
from app.api.routes import video_pitch, rag, competitor
# from app.api.routes import ai_analyzer  # Add when implemented

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(video_pitch.router)
app.include_router(rag.router)
app.include_router(competitor.router)
# app.include_router(ai_analyzer.router)  # Add when implemented

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Analyst Platform API",
        "version": settings.API_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.API_VERSION
    }

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("="*70)
    logger.info("🚀 AI ANALYST PLATFORM - STARTING UP")
    logger.info(f"📍 Version: {settings.API_VERSION}")
    logger.info(f"📁 Upload directory: {settings.UPLOAD_DIR}")
    logger.info(f"💾 ChromaDB path: {settings.CHROMA_DB_PATH}")
    logger.info("="*70)

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("="*70)
    logger.info("👋 AI ANALYST PLATFORM - SHUTTING DOWN")
    logger.info("="*70)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
