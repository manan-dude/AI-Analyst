# app/services/competitor_service.py
from crawl4ai import AsyncWebCrawler
from app.core.clients import gemini_client
from app.config import settings
from app.utils.logger import logger

class CompetitorService:
    """Service for competitor analysis."""
    
    @staticmethod
    async def scrape_website(url: str) -> str:
        """Scrape website content."""
        logger.info(f"🌐 Scraping website: {url}")
        
        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(url=url)
            
        logger.info(f"✅ Scraped {len(result.markdown)} characters")
        return result.markdown[:30000]  # Limit to 30k chars
    
    @staticmethod
    def analyze_competitor(company_name: str, scraped_content: str) -> dict:
        """Analyze competitor using Gemini."""
        logger.info(f"🤖 Analyzing competitor: {company_name}")
        
        analysis_prompt = f"""
You are a competitive intelligence analyst. Analyze the following company website content.

COMPANY: {company_name}

WEBSITE CONTENT:
---
{scraped_content}
---

Provide a comprehensive competitive analysis in JSON format:

{{
    "company_overview": "Brief 2-3 sentence description",
    "business_model": "How they make money",
    "target_audience": "Who are their customers",
    "key_features": ["Feature 1", "Feature 2", "Feature 3"],
    "pricing_strategy": "Pricing model and tiers",
    "technology_stack": "Technologies they use (if mentioned)",
    "competitive_advantages": ["Advantage 1", "Advantage 2"],
    "weaknesses": ["Weakness 1", "Weakness 2"],
    "recent_news": "Any recent updates or announcements"
}}

Output ONLY valid JSON.
"""
        
        response = gemini_client.models.generate_content(
            model=settings.GENERATIVE_MODEL,
            contents=analysis_prompt
        )
        
        # Parse JSON
        raw_text = response.candidates.content.parts.text
        json_text = raw_text.strip()
        
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]
        
        import json
        return json.loads(json_text.strip())

competitor_service = CompetitorService()
