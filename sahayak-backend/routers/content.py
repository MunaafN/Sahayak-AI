from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging
from services.genkit_ai_service import GenkitAIService
from services.speech_service import SpeechService

router = APIRouter()
logger = logging.getLogger(__name__)

class ContentRequest(BaseModel):
    model_config = {"populate_by_name": True}  # Allow both field names and aliases
    
    topic: str
    grade_level: str = Field(alias="gradeLevel")  # Accept both grade_level and gradeLevel
    content_type: Optional[str] = Field(default="content", alias="contentType")  # Accept contentType from frontend
    language: str  # language
    length: str = "medium"  # word limit
    subject: str = "General"  # subject area

class ContentResponse(BaseModel):
    content: str

@router.post("/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """
    Generate hyper-local educational content using Genkit AI (powered by Google Gemini)
    """
    try:
        logger.info(f"Generating content for topic: {request.topic}, grade: {request.grade_level}")
        
        # Initialize Genkit AI service (free with API key!)
        ai_service = GenkitAIService()
        
        # Pass the topic directly to the service
        generated_content = await ai_service.generate_text(
            request.topic,
            language=request.language,
            content_type=request.content_type,
            grade_level=request.grade_level,
            length=request.length,
            subject=request.subject
        )
        
        return ContentResponse(content=generated_content)
        
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {str(e)}")

@router.post("/generate-audio")
async def generate_audio_content(
    topic: str,
    grade_level: str,
    language: str,
    voice: str = "hi-IN-Standard-A"
):
    """
    Generate audio content for the given topic
    """
    try:
        logger.info(f"Generating audio for topic: {topic}")
        
        # Initialize services
        ai_service = GenkitAIService()
        speech_service = SpeechService()
        
        # Generate text content first
        text_content = await ai_service.generate_text(
            topic,
            language=language,
            content_type="story",
            grade_level=grade_level,
            length="medium"
        )
        
        # Convert to audio
        audio_url = await speech_service.generate_speech(text_content, language, voice)
        
        return {
            "text": text_content,
            "audio_url": audio_url,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error generating audio content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate audio content: {str(e)}")

@router.get("/health")
async def content_health():
    """Health check for content generation service"""
    return {"status": "healthy", "service": "content-generation"} 