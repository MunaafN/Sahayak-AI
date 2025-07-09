from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging
import requests
import base64
import os
import time
import uuid
from io import BytesIO
from services.ollama_ai_service import OllamaAIService

router = APIRouter()
logger = logging.getLogger(__name__)

# Hugging Face configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "your-hf-token-here")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
ALTERNATIVE_API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

# Simple HF API configuration (ChatGPT approach)
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY", "your-hf-token-here")
SIMPLE_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
SIMPLE_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
FALLBACK_API_URL = "https://api-inference.huggingface.co/models/playgroundai/playground-v2.5-1024px-aesthetic"

class VisualRequest(BaseModel):
    prompt: str
    style: str
    subject: str

class VisualResponse(BaseModel):
    imageUrl: str
    prompt: str
    style: str
    subject: str

def save_generated_image(image_data: bytes, filename: str) -> str:
    """Save generated image and return URL"""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/visuals"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save image file
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(image_data)
        
        # Return relative URL (adjust based on your server setup)
        return f"/uploads/visuals/{filename}"
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save generated image")

def enhance_prompt_for_education(prompt: str, style: str, subject: str) -> str:
    """Enhance the user prompt for better educational visuals"""
    
    style_modifiers = {
        "illustration": "colorful educational illustration, clear and detailed, suitable for children",
        "diagram": "clean educational diagram with clear labels, professional style, high contrast",
        "cartoon": "child-friendly cartoon style, colorful and engaging, educational",
        "realistic": "realistic educational illustration, detailed but appropriate for students"
    }
    
    subject_context = {
        "science": "scientific accuracy, educational value",
        "mathematics": "clear mathematical concepts, geometric precision",
        "social_studies": "culturally appropriate, historically accurate",
        "language": "clear text and symbols, educational context",
        "geography": "accurate geographical features and representations",
        "history": "historically accurate, appropriate for students"
    }
    
    style_modifier = style_modifiers.get(style, "educational illustration")
    subject_modifier = subject_context.get(subject, "educational value")
    
    enhanced_prompt = f"{prompt}, {style_modifier}, {subject_modifier}, high quality, clear and visible, suitable for Indian school children, educational poster style"
    
    return enhanced_prompt

@router.post("/generate", response_model=VisualResponse)
async def generate_visual(request: VisualRequest):
    """
    Generate educational visual aids using Hugging Face Stable Diffusion 2.1
    """
    try:
        logger.info(f"Generating visual for: {request.prompt[:50]}...")
        print("=" * 60)
        print("🎨 NEW VISUAL GENERATION REQUEST:")
        print(f"   📝 Prompt: {request.prompt}")
        print(f"   🎭 Style: {request.style}")
        print(f"   📚 Subject: {request.subject}")
        print("=" * 60)
        
        # Enhance the prompt for better educational content
        enhanced_prompt = enhance_prompt_for_education(request.prompt, request.style, request.subject)
        print(f"🔄 Enhanced prompt: {enhanced_prompt}")
        
        # Prepare headers for Hugging Face API
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Prepare the payload
        payload = {
            "inputs": enhanced_prompt,
            "parameters": {
                "negative_prompt": "blurry, low quality, inappropriate, violent, scary, dark",
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            },
            "options": {
                "wait_for_model": True,
                "use_cache": False
            }
        }
        
        print("🤖 Calling Hugging Face Stable Diffusion v1.5...")
        
        # Make request to Hugging Face API
        response = requests.post(
            HUGGINGFACE_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"📊 HF API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"📄 HF API Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            # Get image data
            image_data = response.content
            
            # Generate unique filename
            timestamp = int(time.time())
            filename = f"visual_{timestamp}_{request.style}_{request.subject}.jpg"
            
            # Save the image and get URL
            image_url = save_generated_image(image_data, filename)
            
            print("✅ Visual generated successfully!")
            print(f"📁 Saved as: {filename}")
            print(f"🔗 URL: {image_url}")
            print("=" * 60)
            
            return VisualResponse(
                imageUrl=image_url,
                prompt=request.prompt,
                style=request.style,
                subject=request.subject
            )
            
        elif response.status_code == 503:
            # Model is loading, provide fallback
            print("⚠️ Hugging Face model is loading...")
            fallback_url = f"https://via.placeholder.com/512x512/E5E7EB/6B7280?text=Generating+Visual...+Please+wait"
            
            return VisualResponse(
                imageUrl=fallback_url,
                prompt=request.prompt,
                style=request.style,
                subject=request.subject
            )
            
        else:
            # Try alternative model as fallback
            print(f"⚠️ Primary model failed ({response.status_code}), trying alternative...")
            fallback_result = await try_alternative_model(enhanced_prompt, request)
            if fallback_result:
                return fallback_result
            
            error_msg = f"Hugging Face API error: {response.status_code}"
            print(f"❌ {error_msg}")
            logger.error(f"HF API error: {response.status_code}, {response.text}")
            
            # Provide fallback placeholder
            fallback_url = f"https://via.placeholder.com/512x512/FEE2E2/DC2626?text=Generation+Failed"
            
            return VisualResponse(
                imageUrl=fallback_url,
                prompt=request.prompt,
                style=request.style,
                subject=request.subject
            )
        
    except requests.exceptions.Timeout:
        print("⏱️ Hugging Face API timeout")
        fallback_url = f"https://via.placeholder.com/512x512/FEF3C7/D97706?text=Timeout+-+Try+Again"
        
        return VisualResponse(
            imageUrl=fallback_url,
            prompt=request.prompt,
            style=request.style,
            subject=request.subject
        )
        
    except Exception as e:
        error_msg = f"Failed to generate visual: {str(e)}"
        logger.error(f"Error generating visual: {str(e)}")
        print(f"❌ {error_msg}")
        
        # Provide fallback placeholder
        fallback_url = f"https://via.placeholder.com/512x512/FEE2E2/DC2626?text=Error+Occurred"
        
        return VisualResponse(
            imageUrl=fallback_url,
            prompt=request.prompt,
            style=request.style,
            subject=request.subject
        )

async def try_alternative_model(enhanced_prompt: str, request: VisualRequest):
    """Try alternative Stable Diffusion model as fallback"""
    try:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": enhanced_prompt,
            "parameters": {
                "num_inference_steps": 15,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            },
            "options": {
                "wait_for_model": True,
                "use_cache": False
            }
        }
        
        print("🔄 Trying alternative model: CompVis/stable-diffusion-v1-4...")
        
        response = requests.post(
            ALTERNATIVE_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )
        
        print(f"📊 Alternative API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            image_data = response.content
            
            # Generate unique filename
            timestamp = int(time.time())
            filename = f"visual_alt_{timestamp}_{request.style}_{request.subject}.jpg"
            
            # Save the image and get URL
            image_url = save_generated_image(image_data, filename)
            
            print("✅ Alternative model generated visual successfully!")
            print(f"📁 Saved as: {filename}")
            print(f"🔗 URL: {image_url}")
            
            return VisualResponse(
                imageUrl=image_url,
                prompt=request.prompt,
                style=request.style,
                subject=request.subject
            )
        else:
            print(f"❌ Alternative model also failed: {response.status_code}")
            logger.error(f"Alternative model failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Alternative model error: {str(e)}")
        logger.error(f"Alternative model error: {str(e)}")
        return None

@router.get("/generate-image")
async def generate_image(prompt: str = Query(..., description="Image generation prompt")):
    """
    Simple image generation endpoint using GET request
    Usage: /api/visuals/generate-image?prompt=your+text
    """
    try:
        print("=" * 60)
        print("🎨 SIMPLE IMAGE GENERATION REQUEST:")
        print(f"   📝 Prompt: {prompt}")
        print("=" * 60)
        
        # Call Hugging Face API with simple structure
        print("🤖 Calling Hugging Face FLUX.1-schnell...")
        response = requests.post(
            SIMPLE_API_URL, 
            headers=SIMPLE_HEADERS, 
            json={
                "inputs": prompt,
                "options": {"wait_for_model": True}
            },
            timeout=60
        )
        
        print(f"📊 HF API Response Status: {response.status_code}")
        if response.status_code == 200:
            print(f"📊 Image received: {len(response.content)} bytes")
        
        if response.status_code != 200:
            print(f"❌ FLUX failed, trying Playground v2.5...")
            # Try fallback model
            response = requests.post(
                FALLBACK_API_URL, 
                headers=SIMPLE_HEADERS, 
                json={
                    "inputs": prompt,
                    "options": {"wait_for_model": True}
                },
                timeout=60
            )
            print(f"📊 Fallback API Response Status: {response.status_code}")
            if response.status_code == 200:
                print(f"📊 Fallback image received: {len(response.content)} bytes")
            
            if response.status_code != 200:
                print(f"❌ Both models failed: {response.text[:200]}")
                # Generate a placeholder image instead of failing
                return await create_placeholder_image(prompt)

        # Check if we have a successful response with image data
        if response.status_code == 200 and len(response.content) > 0:
            print("✅ Got successful image response, processing...")
            
            # Create uploads directory if it doesn't exist
            upload_dir = "uploads/visuals"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the image with unique name
            image_name = f"generated_{uuid.uuid4().hex[:8]}.png"
            image_path = os.path.join(upload_dir, image_name)
            
            with open(image_path, "wb") as f:
                f.write(response.content)

            # Create the server URL for the saved image
            image_url = f"/uploads/visuals/{image_name}"
            
            print(f"✅ Image generated successfully!")
            print(f"📁 Saved as: {image_path}")
            print(f"🔗 Server URL: {image_url}")
            print("=" * 60)

            # Return JSON with image URL instead of the file
            return JSONResponse(
                content={
                    "imageUrl": image_url,
                    "success": True,
                    "message": "Visual generated successfully"
                },
                headers={"Content-Type": "application/json"}
            )
        else:
            # If we get here, something went wrong
            print(f"❌ Invalid response: status={response.status_code}, content_length={len(response.content)}")
            return await create_placeholder_image(prompt)

    except requests.exceptions.Timeout:
        print("⏱️ Request timeout")
        return JSONResponse(
            status_code=500, 
            content={"error": "Request timeout - please try again"},
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)},
            headers={"Content-Type": "application/json"}
        )

@router.get("/health")
async def visuals_health():
    """Health check for visual generation service"""
    return {"status": "healthy", "service": "visual-generation", "provider": "Hugging Face FLUX.1-schnell"}

@router.get("/test-models")
async def test_models():
    """Test available models"""
    test_results = {}
    models_to_test = [
        ("black-forest-labs/FLUX.1-schnell", SIMPLE_API_URL),
        ("playgroundai/playground-v2.5-1024px-aesthetic", FALLBACK_API_URL)
    ]
    
    for model_name, url in models_to_test:
        try:
            response = requests.post(
                url,
                headers=SIMPLE_HEADERS,
                json={"inputs": "test prompt", "options": {"wait_for_model": True}},
                timeout=30
            )
            test_results[model_name] = {
                "status": response.status_code,
                "available": response.status_code == 200,
                "response": response.text[:100] if response.status_code != 200 else "OK"
            }
        except Exception as e:
            test_results[model_name] = {
                "status": "error",
                "available": False,
                "response": str(e)
            }
    
    return {"model_tests": test_results}

async def create_placeholder_image(prompt: str):
    """Create a placeholder image when AI generation fails"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
        
        # Create a 512x512 image with educational theme
        width, height = 512, 512
        image = Image.new('RGB', (width, height), color='#f8f9fa')
        draw = ImageDraw.Draw(image)
        
        # Try to use a better font, fallback to default
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw educational-themed border
        border_color = '#4f46e5'  # Primary color
        draw.rectangle([10, 10, width-10, height-10], outline=border_color, width=3)
        
        # Add title
        title = "📚 Educational Visual"
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 50), title, fill=border_color, font=font_large)
        
        # Add prompt (wrapped)
        wrapped_prompt = textwrap.fill(prompt[:100], width=40)
        prompt_lines = wrapped_prompt.split('\n')
        
        y_offset = 120
        for line in prompt_lines[:4]:  # Max 4 lines
            line_bbox = draw.textbbox((0, 0), line, font=font_small)
            line_width = line_bbox[2] - line_bbox[0]
            draw.text(((width - line_width) // 2, y_offset), line, fill='#374151', font=font_small)
            y_offset += 25
        
        # Add message
        message = "🔧 AI Image Generation Temporarily Unavailable"
        message_bbox = draw.textbbox((0, 0), message, font=font_small)
        message_width = message_bbox[2] - message_bbox[0]
        draw.text(((width - message_width) // 2, height - 100), message, fill='#dc2626', font=font_small)
        
        # Add instruction
        instruction = "Please try again later or check with your teacher"
        inst_bbox = draw.textbbox((0, 0), instruction, font=font_small)
        inst_width = inst_bbox[2] - inst_bbox[0]
        draw.text(((width - inst_width) // 2, height - 70), instruction, fill='#6b7280', font=font_small)
        
        # Save placeholder image
        upload_dir = "uploads/visuals"
        os.makedirs(upload_dir, exist_ok=True)
        
        image_name = f"placeholder_{uuid.uuid4().hex[:8]}.png"
        image_path = os.path.join(upload_dir, image_name)
        image.save(image_path, "PNG")
        
        # Create the server URL for the placeholder image
        image_url = f"/uploads/visuals/{image_name}"
        
        print(f"✅ Generated placeholder image: {image_path}")
        print(f"🔗 Placeholder URL: {image_url}")
        
        return JSONResponse(
            content={
                "imageUrl": image_url,
                "success": True,
                "message": "Placeholder visual generated"
            },
            headers={"Content-Type": "application/json"}
        )
        
    except Exception as e:
        print(f"❌ Failed to create placeholder: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"error": "Image generation and fallback both failed"},
            headers={"Content-Type": "application/json"}
        ) 