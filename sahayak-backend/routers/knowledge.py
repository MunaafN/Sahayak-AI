from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.ollama_ai_service import OllamaAIService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class QuestionRequest(BaseModel):
    question: str  # question
    complexity: str = "medium"  # complexity level  
    language: str  # answer language
    length: str = "medium"  # answer length

class AnswerResponse(BaseModel):
    answer: str
    question: str
    language: str
    complexity: str  # complexity level instead of gradeLevel

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Answer questions with simple, age-appropriate explanations
    """
    try:
        logger.info(f"Processing question: {request.question[:50]}...")
        
        # Initialize Ollama AI service
        ollama_ai = OllamaAIService()
        
        # Generate answer using Ollama AI - let the service handle prompt creation
        answer = await ollama_ai.generate_text(
            request.question,
            language=request.language,
            grade_level=request.complexity, # Assuming complexity maps to grade_level for now
            content_type="answer",
            length=request.length
        )
        
        return AnswerResponse(
            answer=answer,
            question=request.question,
            language=request.language,
            complexity=request.complexity # Assuming complexity maps to grade_level for now
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")

@router.get("/health")
async def knowledge_health():
    """Health check for knowledge base service"""
    return {"status": "healthy", "service": "knowledge-base"} 