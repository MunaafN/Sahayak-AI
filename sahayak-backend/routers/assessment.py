from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from services.genkit_ai_service import GenkitAIService
from services.speech_service import SpeechService

router = APIRouter()
logger = logging.getLogger(__name__)

class AssessmentResponse(BaseModel):
    overall_score: float
    fluency_score: float
    accuracy_score: float
    pronunciation_score: float
    pace_score: float
    transcription: str
    feedback: str
    missed_words: List[str]

class TextGenerationRequest(BaseModel):
    grade_level: str  # grade level
    language: str  # language
    difficulty: str = "medium"
    word_limit: str = "medium"  # word limit

class TextGenerationResponse(BaseModel):
    text: str

@router.post("/analyze", response_model=AssessmentResponse)
async def analyze_reading(
    audio: UploadFile = File(...),
    original_text: str = Form(...),
    language: str = Form(...),
    grade_level: str = Form(...)
):
    """
    Analyze reading performance from audio recording
    """
    try:
        logger.info(f"Processing reading assessment for grade {grade_level}")
        
        # Initialize services
        speech_service = SpeechService()
        ai_service = GenkitAIService()
        
        # Convert audio to text
        audio_content = await audio.read()
        transcription = await speech_service.transcribe_audio(audio_content, language)
        
        # Analyze reading fluency
        fluency_analysis = await speech_service.analyze_reading_fluency(original_text, transcription)
        
        # Generate detailed feedback using AI
        analysis_prompt = f"""
        Analyze this reading assessment for a Grade {grade_level} student:
        
        Original Text: {original_text}
        Student's Reading (transcribed): {transcription}
        Language: {language}
        
        Basic Analysis:
        - Accuracy: {fluency_analysis['accuracy']}%
        - Correct Words: {fluency_analysis['correct_words']}/{fluency_analysis['total_words']}
        
        Please provide specific, constructive feedback in {language} that:
        1. Acknowledges what the student did well
        2. Identifies specific areas for improvement
        3. Gives practical tips for better reading
        4. Is encouraging and age-appropriate for grade {grade_level}
        
        Keep the feedback concise but helpful (2-3 sentences).
        """
        
        # Get AI-generated feedback
        feedback = await ai_service.generate_text(
            analysis_prompt,
            grade_level=grade_level,
            language=language,
            content_type="feedback",
            length="medium"
        )
        
        # Calculate detailed scores
        accuracy_score = fluency_analysis['accuracy']
        fluency_score = max(0, accuracy_score - 5)  # Slightly lower than accuracy
        pronunciation_score = max(0, accuracy_score - 3)  # Based on word recognition
        pace_score = min(100, accuracy_score + 5)  # Slightly higher if they read well
        overall_score = (accuracy_score + fluency_score + pronunciation_score + pace_score) / 4
        
        # Extract missed words
        missed_words = [mistake['expected'] for mistake in fluency_analysis['mistakes']]
        
        return AssessmentResponse(
            overall_score=round(overall_score, 1),
            fluency_score=round(fluency_score, 1),
            accuracy_score=round(accuracy_score, 1),
            pronunciation_score=round(pronunciation_score, 1),
            pace_score=round(pace_score, 1),
            transcription=transcription,
            feedback=feedback,
            missed_words=missed_words[:5]  # Limit to top 5 missed words
        )
        
    except Exception as e:
        logger.error(f"Error in reading assessment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to assess reading: {str(e)}")

@router.post("/generate-text", response_model=TextGenerationResponse)
async def generate_reading_text(request: TextGenerationRequest):
    """
    Generate age-appropriate reading text for assessment
    """
    try:
        logger.info(f"Generating reading text for grade {request.grade_level}")
        
        # Initialize Genkit AI service
        ai_service = GenkitAIService()
        
        # Define complexity levels
        complexity_map = {
            "1": "very simple sentences with 3-5 words each",
            "2": "simple sentences with basic vocabulary",
            "3": "moderate sentences with elementary vocabulary",
            "4": "compound sentences with intermediate vocabulary",
            "5": "complex sentences with advanced elementary vocabulary"
        }
        
        difficulty_map = {
            "easy": "simple and repetitive",
            "medium": "moderately challenging", 
            "hard": "appropriately challenging"
        }
        
        word_limit_map = {
            "short": "50-100 words",
            "medium": "100-150 words", 
            "long": "150-200 words"
        }
        
        complexity = complexity_map.get(request.grade_level, "simple sentences")
        difficulty_level = difficulty_map.get(request.difficulty, "moderately challenging")
        target_length = word_limit_map.get(request.word_limit, "100-150 words")
        
        # Create prompt for text generation
        prompt = f"""
        Generate a {difficulty_level} reading passage for Grade {request.grade_level} students in {request.language}.
        
        Requirements:
        - Use {complexity}
        - Length: {target_length}
        - Educational content (science, nature, friendship, family values)
        - Include Indian cultural context and familiar scenarios
        - Make it engaging and age-appropriate
        - Use proper grammar and punctuation
        
        If the language is Hindi or Marathi, write completely in that script.
        
        Create a story or informational text that would be interesting for children to read aloud.
        """
        
        # Generate text using Genkit AI
        generated_text = await ai_service.generate_text(
            prompt,
            grade_level=request.grade_level,
            language=request.language,
            content_type="reading_passage",
            length=request.word_limit
        )
        
        return TextGenerationResponse(text=generated_text)
        
    except Exception as e:
        logger.error(f"Error generating reading text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate text: {str(e)}")

@router.get("/health")
async def assessment_health():
    """Health check for assessment service"""
    return {"status": "healthy", "service": "reading-assessment"} 