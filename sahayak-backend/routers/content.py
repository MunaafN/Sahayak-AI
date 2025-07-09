from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from services.ollama_ai_service import OllamaAIService
from services.speech_service import SpeechService

router = APIRouter()
logger = logging.getLogger(__name__)

class ContentRequest(BaseModel):
    topic: str  # topic/subject
    contentType: str  # content type
    gradeLevel: str  # grade level
    language: str  # language
    length: str = "medium"  # answer length

class ContentResponse(BaseModel):
    content: str
    language: str
    gradeLevel: str
    topic: str

class TTSRequest(BaseModel):
    text: str
    language: str

class TTSResponse(BaseModel):
    audioConfig: str
    success: bool

@router.post("/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """
    Generate hyper-local educational content using Ollama AI (completely free!)
    """
    try:
        logger.info(f"Generating content for topic: {request.topic}")
        
        # Initialize Ollama AI service (completely free, no limits!)
        ollama_ai = OllamaAIService()
        
        # Pass the topic directly to the service
        generated_content = await ollama_ai.generate_text(
            request.topic, 
            language=request.language,
            content_type=request.contentType,
            grade_level=request.gradeLevel,
            length=request.length
        )
        
        return ContentResponse(
            content=generated_content,
            language=request.language,
            gradeLevel=request.gradeLevel,
            topic=request.topic
        )
        
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {str(e)}")

@router.post("/text-to-speech", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech for read aloud functionality
    """
    try:
        logger.info(f"Converting text to speech: {request.text[:50]}...")
        
        # Initialize Speech service
        speech_service = SpeechService()
        
        # Generate TTS configuration
        audio_config = await speech_service.text_to_speech(request.text, request.language)
        
        return TTSResponse(
            audioConfig=audio_config,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}")
        # Return fallback configuration for client-side TTS
        import json
        import base64
        fallback_config = {
            "text": request.text,
            "lang": "en-US" if request.language == "en" else f"{request.language}-IN",
            "rate": 0.8,
            "pitch": 1.0,
            "volume": 1.0,
            "useWebSpeechAPI": True
        }
        config_json = json.dumps(fallback_config)
        config_b64 = base64.b64encode(config_json.encode()).decode()
        
        return TTSResponse(
            audioConfig=config_b64,
            success=True
        )

@router.get("/health")
async def content_health():
    """Health check for content generation service"""
    return {"status": "healthy", "service": "content-generation"} 