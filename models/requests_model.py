# app/models/request_models.py
from pydantic import BaseModel, Field, validator

class VideoPitchRequest(BaseModel):
    youtube_url: str = Field(..., description="YouTube video URL")
    
    @validator('youtube_url')
    def validate_youtube_url(cls, v):
        if 'youtube.com' not in v and 'youtu.be' not in v:
            raise ValueError('Invalid YouTube URL')
        return v

class CompetitorRequest(BaseModel):
    company_name: str = Field(..., min_length=1, description="Target company name")
    company_url: str = Field(..., description="Target company website URL")

class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User question")
    collection_name: str = Field(default="user_documents", description="Collection to query")
