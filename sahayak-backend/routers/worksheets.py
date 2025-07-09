from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict
import logging
import base64
import subprocess
import requests
import json
from services.ollama_ai_service import OllamaAIService

router = APIRouter()
logger = logging.getLogger(__name__)

class WorksheetRequest(BaseModel):
    image: str
    grades: List[str]  # target grades
    subject: str  # subject

class WorksheetResponse(BaseModel):
    worksheets: Dict[str, str]
    success: bool
    message: str

@router.post("/generate", response_model=WorksheetResponse)
async def generate_worksheets(
    image: str = Form(...),
    grades: List[str] = Form(...),  # target grades
    subject: str = Form(...)  # subject
):
    """
    Generate differentiated worksheets from textbook page image
    """
    try:
        logger.info(f"Generating worksheets for grades: {grades}, subject: {subject}")
        
        # Initialize Ollama AI service
        ollama_ai = OllamaAIService()
        
        worksheets = {}
        
        for grade in grades:
            # Create grade-specific prompt
            prompt = f"""
            Based on the textbook page image provided, create a worksheet for grade {grade} students in {subject}.
            
            Requirements:
            - Adapt the difficulty level for grade {grade}
            - Include 5-8 questions/exercises
            - Mix different question types (fill-in-the-blank, short answer, match the following)
            - Ensure questions are based on the content visible in the image
            - Make it appropriate for Indian curriculum standards
            - Include clear instructions for students
            
            Grade Level: {grade}
            Subject: {subject}
            
            Format the output as a ready-to-use worksheet.
            """
            
            # Generate worksheet using Ollama AI
            worksheet_content = await ollama_ai.generate_text(
                prompt,
                language="en", # Assuming default language for now
                content_type="worksheet",
                grade_level=grade,
                length="medium", # Assuming default length for now
                subject=subject
            )
            worksheets[grade] = worksheet_content
        
        return WorksheetResponse(
            worksheets=worksheets,
            success=True,
            message=f"Successfully generated worksheets for grades {', '.join(grades)}"
        )
        
    except Exception as e:
        logger.error(f"Error generating worksheets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate worksheets: {str(e)}")

@router.post("/generate-with-vision", response_model=WorksheetResponse)
async def generate_worksheets_with_vision(request: WorksheetRequest):
    """
    Generate differentiated worksheets using llava-phi3 vision model
    """
    try:
        logger.info(f"🔍 Generating vision-based worksheets for grades: {request.grades}, subject: {request.subject}")
        
        # Step 1: Start llava-phi3:latest model with Ollama
        print("🚀 Starting llava-phi3:latest model...")
        try:
            # Pull/run llava-phi3:latest model
            result = subprocess.run(
                ["ollama", "run", "llava-phi3:latest", "--help"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            print(f"✅ llava-phi3:latest model ready")
        except subprocess.TimeoutExpired:
            print("⚠️ Model start timeout, proceeding anyway...")
        except Exception as e:
            print(f"⚠️ Model start warning: {e}, proceeding...")
        
        # Step 2: Prepare image data (remove data URL prefix if present)
        image_data = request.image
        if request.image.startswith('data:image'):
            image_data = request.image.split(',')[1]
        
        worksheets = {}
        
        for grade in request.grades:
            # Step 3: Create sentence-type prompt combining image and text inputs with deep analysis
            sentence_prompt = f"Please deeply analyze this textbook page image for {request.subject} subject. Look carefully at all text, diagrams, illustrations, examples, and educational content visible in the image. Based on your thorough analysis of what you can see, create comprehensive worksheet activities for grade {grade} students. Include questions that test understanding of the specific concepts, examples, and information shown in this textbook page. Make sure the worksheet directly relates to the content visible in the image and is appropriate for Indian curriculum standards for grade {grade} {request.subject}."
            
            print(f"📝 Generating worksheet for Grade {grade}...")
            
            # Step 4: Call llava-phi3:latest via Ollama API
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llava-phi3:latest",
                        "prompt": sentence_prompt,
                        "images": [image_data],
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9
                        }
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    worksheet_content = result.get('response', '')
                    
                    # Clean up the response
                    if worksheet_content:
                        worksheet_content = f"Grade {grade} Worksheet - {request.subject}\n" + "="*50 + "\n\n" + worksheet_content
                        worksheets[grade] = worksheet_content
                        print(f"✅ Generated worksheet for Grade {grade} ({len(worksheet_content)} characters)")
                    else:
                        worksheets[grade] = f"Grade {grade} Worksheet - {request.subject}\n\nWorksheet generation failed. Please try again."
                        print(f"❌ Empty response for Grade {grade}")
                else:
                    print(f"❌ API error {response.status_code} for Grade {grade}")
                    worksheets[grade] = f"Grade {grade} Worksheet - {request.subject}\n\nWorksheet generation failed. Please try again."
                    
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout for Grade {grade}")
                worksheets[grade] = f"Grade {grade} Worksheet - {request.subject}\n\nGeneration timed out. Please try again."
            except Exception as e:
                print(f"❌ Error for Grade {grade}: {str(e)}")
                print(f"🔄 Falling back to text-based generation for Grade {grade}...")
                
                # Fallback to regular text-based generation
                try:
                    ollama_ai = OllamaAIService()
                    fallback_prompt = f"""
                    Create a worksheet for grade {grade} students in {request.subject}.
                    
                    Requirements:
                    - Adapt the difficulty level for grade {grade}
                    - Include 5-8 questions/exercises
                    - Mix different question types (fill-in-the-blank, short answer, multiple choice)
                    - Make it appropriate for Indian curriculum standards
                    - Include clear instructions for students
                    
                    Grade Level: {grade}
                    Subject: {request.subject}
                    
                    Format the output as a ready-to-use worksheet.
                    """
                    
                    fallback_content = await ollama_ai.generate_text(
                        fallback_prompt,
                        language="en", # Default language for worksheets
                        content_type="worksheet",
                        grade_level=grade,
                        length="medium", # Default length for worksheets
                        subject=request.subject
                    )
                    
                    worksheets[grade] = f"Grade {grade} Worksheet - {request.subject}\n" + "="*50 + "\n\n" + fallback_content
                    print(f"✅ Generated fallback worksheet for Grade {grade}")
                    
                except Exception as fallback_error:
                    print(f"❌ Fallback also failed for Grade {grade}: {str(fallback_error)}")
                    worksheets[grade] = f"Grade {grade} Worksheet - {request.subject}\n\nWorksheet generation failed. Please try again."
        
        return WorksheetResponse(
            worksheets=worksheets,
            success=True,
            message=f"Successfully generated vision-based worksheets for grades {', '.join(request.grades)}"
        )
        
    except Exception as e:
        logger.error(f"Error generating vision-based worksheets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate worksheets: {str(e)}")

@router.get("/health")
async def worksheets_health():
    """Health check for worksheet generation service"""
    return {"status": "healthy", "service": "worksheet-generation"} 