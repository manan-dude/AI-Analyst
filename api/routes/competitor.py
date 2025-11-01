# app/api/routes/competitor.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.request_models import CompetitorRequest
from app.services.competitor_service import competitor_service
from app.utils.logger import logger

router = APIRouter(prefix="/api/competitor", tags=["Competitor Analysis"])

@router.post("/analyze")
async def analyze_competitor(request: CompetitorRequest):
    """Analyze competitor website."""
    logger.info("="*70)
    logger.info(f"🔍 COMPETITOR ANALYSIS: {request.company_name}")
    
    try:
        # Scrape website
        scraped_content = await competitor_service.scrape_website(request.company_url)
        
        # Analyze
        analysis_data = competitor_service.analyze_competitor(
            request.company_name,
            scraped_content
        )
        
        analysis_data['company_name'] = request.company_name
        analysis_data['company_url'] = request.company_url
        
        logger.info("✅ Competitor analysis completed")
        return JSONResponse(content={"success": True, "data": analysis_data})
        
    except Exception as e:
        logger.error(f"❌ Competitor analysis failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
