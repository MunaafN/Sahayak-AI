from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import logging
from services.ollama_ai_service import OllamaAIService

router = APIRouter()
logger = logging.getLogger(__name__)

class LessonRequest(BaseModel):
    topic: str  # topic
    subject: str  # subject
    grade_level: str  # grade level
    language: str = "en"  # language
    length: str = "medium"

class LessonPlanResponse(BaseModel):
    lesson_plan: str
    topic: str
    subject: str
    grade_level: str
    language: str

@router.post("/generate", response_model=LessonPlanResponse)
async def generate_lesson_plan(request: LessonRequest):
    """
    Generate a comprehensive lesson plan using Ollama AI (completely free!)
    """
    try:
        logger.info(f"Generating lesson for subject: {request.subject}")
        
        # Initialize Ollama AI service
        ollama_ai = OllamaAIService()
        
        # Generate lesson plan using Ollama AI with the specific topic and subject
        lesson_plan = await ollama_ai.generate_text(
            request.topic,  # Pass the actual topic/theme entered by user
            language=request.language,
            content_type="lesson_plan",
            grade_level=request.grade_level,
            subject=request.subject,  # Pass subject as additional parameter
            length=request.length
        )
        
        return LessonPlanResponse(
            lesson_plan=lesson_plan,
            topic=request.topic,
            subject=request.subject,
            grade_level=request.grade_level,
            language=request.language
        )
        
    except Exception as e:
        logger.error(f"Error generating lesson: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate lesson: {str(e)}")

@router.get("/health")
async def lessons_health():
    """Health check for lesson planning service"""
    return {"status": "healthy", "service": "lesson-planning"} 