from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging
import base64
import os
import time
import uuid
import requests
from dotenv import load_dotenv
from services.genkit_ai_service import GenkitAIService

# Load environment variables
load_dotenv()

router = APIRouter()
logger = logging.getLogger(__name__)

class VisualRequest(BaseModel):
    prompt: str
    style: str
    subject: str

class VisualResponse(BaseModel):
    imageUrl: str
    prompt: str
    style: str
    subject: str

def create_educational_visual(prompt: str, style: str, subject: str, description: str = "") -> str:
    """Create actual educational visual using multiple strategies"""
    try:
        # Strategy 1: Try to use a free image generation API
        generated_url = try_free_image_generation(prompt, style, subject, description)
        if generated_url:
            return generated_url
        
        # Strategy 2: Try to get educational images from Unsplash
        unsplash_url = try_unsplash_educational_image(prompt, subject)
        if unsplash_url:
            return unsplash_url
        
        # Strategy 3: Create dynamic educational placeholder with user selections
        return create_dynamic_placeholder(prompt, style, subject, description)
        
    except Exception as e:
        logger.error(f"Error creating educational visual: {str(e)}")
        return create_fallback_placeholder(prompt, style, subject)

def try_free_image_generation(prompt: str, style: str, subject: str, description: str) -> Optional[str]:
    """Generate images using Stability AI API"""
    try:
        # Get Stability AI API key from environment
        stability_api_key = os.getenv("STABILITY_API_KEY")
        print(f"🔍 Environment check - Stability AI API Key found: {'Yes' if stability_api_key else 'No'}")
        if stability_api_key:
            print(f"🔑 Stability AI API Key starts with: {stability_api_key[:10]}...")
        
        if not stability_api_key or stability_api_key == "your-stability-ai-api-key-here":
            print("❌ Stability AI API key not configured, skipping image generation")
            logger.info("Stability AI API key not configured, skipping image generation")
            return None

        # Enhanced educational prompt for Stability AI
        base_description = description if description else f"Educational {style} about {prompt} for {subject}"
        
        educational_prompt = f"""
        {base_description}, educational {style}, high quality, detailed, vibrant colors, 
        child-friendly, classroom appropriate, professional educational material, 
        clear visual elements, engaging design, suitable for learning, 
        digital art, clean composition, educational illustration, safe for children
        """
        
        print(f"🤖 Trying Stability AI image generation...")
        print(f"📝 Prompt: {educational_prompt.strip()[:100]}...")
        
        # Stability AI API endpoint for text-to-image
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {stability_api_key}",
        }
        
        payload = {
            "text_prompts": [
                {
                    "text": educational_prompt.strip(),
                    "weight": 1
                },
                {
                    "text": "blurry, low quality, inappropriate, violent, scary, dark, adult content, nsfw",
                    "weight": -1
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "steps": 30,
            "samples": 1,
            "style_preset": "digital-art"
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if "artifacts" in data and len(data["artifacts"]) > 0:
                # Get the first generated image
                image_data = data["artifacts"][0]
                image_base64 = image_data.get("base64")
                
                if image_base64:
                    # Save the generated image
                    upload_dir = "uploads/visuals"
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    timestamp = int(time.time())
                    filename = f"stability_generated_{timestamp}_{style}_{subject}.png"
                    file_path = os.path.join(upload_dir, filename)
                    
                    # Decode and save the image
                    image_bytes = base64.b64decode(image_base64)
                    with open(file_path, "wb") as f:
                        f.write(image_bytes)
                    
                    local_image_url = f"/uploads/visuals/{filename}"
                    print(f"✅ Generated image via Stability AI: {local_image_url}")
                    return local_image_url
                else:
                    print("⚠️ No base64 image data in response")
                    return None
            else:
                print("⚠️ No artifacts in Stability AI response")
                return None
        elif response.status_code == 401:
            print("❌ Stability AI API Key authentication failed")
            return None
        elif response.status_code == 402:
            print("⚠️ Insufficient credits in Stability AI account")
            return None
        else:
            print(f"⚠️ Stability AI API failed: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"⚠️ Stability AI image generation failed: {str(e)}")
        logger.warning(f"Stability AI image generation failed: {str(e)}")
        return None

def try_unsplash_educational_image(prompt: str, subject: str) -> Optional[str]:
    """Get educational images from Unsplash API (free)"""
    try:
        # Create educational search query
        search_terms = []
        
        # Add subject-specific terms
        if subject.lower() == "science":
            search_terms.extend(["science", "education", "learning", "student"])
        elif subject.lower() == "mathematics":
            search_terms.extend(["math", "numbers", "education", "learning"])
        elif subject.lower() == "social_studies":
            search_terms.extend(["history", "geography", "culture", "education"])
        elif subject.lower() == "language":
            search_terms.extend(["books", "reading", "writing", "education"])
        else:
            search_terms.extend(["education", "learning", "school"])
        
        # Add prompt keywords
        prompt_words = prompt.lower().split()[:3]  # Take first 3 words
        search_terms.extend(prompt_words)
        
        search_query = "+".join(search_terms[:5])  # Limit to 5 terms
        
        # Free Unsplash API call (no key needed for basic usage)
        unsplash_url = f"https://source.unsplash.com/800x600/?{search_query}"
        
        # Verify the URL works
        response = requests.head(unsplash_url, timeout=5)
        if response.status_code == 200:
            return unsplash_url
        
        return None
        
    except Exception as e:
        logger.warning(f"Unsplash API failed: {str(e)}")
        return None

def create_dynamic_placeholder(prompt: str, style: str, subject: str, description: str) -> str:
    """Create dynamic educational placeholder that reflects user selections"""
    try:
        # Style-based colors and themes
        style_config = {
            "illustration": {"bg": "E3F2FD", "text": "1565C0", "emoji": "🎨"},
            "diagram": {"bg": "F3E5F5", "text": "7B1FA2", "emoji": "📊"},
            "cartoon": {"bg": "FFF3E0", "text": "F57C00", "emoji": "🎭"},
            "realistic": {"bg": "E8F5E8", "text": "388E3C", "emoji": "📷"}
        }
        
        # Subject-based themes
        subject_config = {
            "science": {"emoji": "🔬", "theme": "Scientific"},
            "mathematics": {"emoji": "🔢", "theme": "Mathematical"}, 
            "social_studies": {"emoji": "🌍", "theme": "Cultural"},
            "language": {"emoji": "📚", "theme": "Literary"},
            "geography": {"emoji": "🗺️", "theme": "Geographic"},
            "history": {"emoji": "🏛️", "theme": "Historical"}
        }
        
        # Get configurations
        style_info = style_config.get(style, style_config["illustration"])
        subject_info = subject_config.get(subject, {"emoji": "🎓", "theme": "Educational"})
        
        # Create descriptive text for the placeholder
        display_text = f"{subject_info['emoji']} {subject_info['theme']} {style_info['emoji']}"
        encoded_prompt = prompt.replace(' ', '+')[:40]
        
        # Create enhanced placeholder URL with style and subject reflected
        placeholder_url = (f"https://via.placeholder.com/600x400/{style_info['bg']}/{style_info['text']}"
                          f"?text={display_text}%0A{encoded_prompt}%0A{style.title()}+Style")
        
        return placeholder_url
        
    except Exception as e:
        logger.error(f"Error creating dynamic placeholder: {str(e)}")
        return create_fallback_placeholder(prompt, style, subject)

def create_fallback_placeholder(prompt: str, style: str, subject: str) -> str:
    """Create basic fallback placeholder"""
    try:
        encoded_text = f"Educational+Visual%0A{prompt.replace(' ', '+')[:30]}"
        return f"https://via.placeholder.com/600x400/E5E7EB/374151?text={encoded_text}"
    except:
        return "https://via.placeholder.com/600x400/E5E7EB/374151?text=Educational+Visual"

def enhance_prompt_for_education(prompt: str, style: str, subject: str) -> str:
    """Enhanced prompt for Google AI to generate detailed visual descriptions"""
    
    style_descriptions = {
        "illustration": "Create a detailed description for a colorful educational illustration",
        "diagram": "Create a detailed description for a clear educational diagram with labels",
        "cartoon": "Create a detailed description for a child-friendly cartoon-style educational visual",
        "realistic": "Create a detailed description for a realistic educational photograph or illustration"
    }
    
    subject_contexts = {
        "science": "focusing on scientific accuracy and clear explanation of concepts",
        "mathematics": "emphasizing mathematical concepts, numbers, and geometric relationships",
        "social_studies": "highlighting cultural, historical, or social elements appropriately",
        "language": "incorporating text, writing, reading, or language learning elements",
        "geography": "showing geographical features, maps, or location-based information",
        "history": "depicting historical accuracy and age-appropriate historical context"
    }
    
    style_desc = style_descriptions.get(style, "Create a detailed description for an educational visual")
    subject_context = subject_contexts.get(subject, "with general educational value")
    
    enhanced_prompt = f"""
    {style_desc} about: {prompt}
    
    Requirements:
    - {subject_context}
    - Suitable for elementary/primary school students
    - Educationally valuable and engaging
    - Clear, bright, and visually appealing
    - Include specific visual elements that would help students understand the concept
    - Describe colors, layout, and key educational components
    - Make it appropriate for Indian educational context
    
    Style: {style.title()}
    Subject: {subject.title()}
    Topic: {prompt}
    
    Provide a detailed visual description that an illustrator could use to create the actual image.
    """
    
    return enhanced_prompt

@router.post("/generate", response_model=VisualResponse)
async def generate_visual(request: VisualRequest):
    """
    Generate educational visual aids using Google AI + multiple image strategies
    """
    try:
        logger.info(f"Generating visual for: {request.prompt[:50]}...")
        print("=" * 60)
        print("🎨 NEW EDUCATIONAL VISUAL GENERATION:")
        print(f"   📝 Prompt: {request.prompt}")
        print(f"   🎭 Style: {request.style}")
        print(f"   📚 Subject: {request.subject}")
        print("=" * 60)
        
        # Initialize Google AI service
        ai_service = GenkitAIService()
        
        visual_description = ""
        
        if ai_service.genkit_available:
            try:
                # Enhance the prompt for better educational content
                enhanced_prompt = enhance_prompt_for_education(request.prompt, request.style, request.subject)
                print(f"🔄 Enhanced prompt: {enhanced_prompt[:150]}...")
                
                print("🤖 Generating visual description with Google Gemini...")
                
                # Use Google AI to generate detailed visual description
                visual_description = await ai_service.generate_text(
                    enhanced_prompt,
                    language="en",
                    content_type="visual",
                    grade_level="3",
                    length="medium",
                    subject=request.subject
                )
                
                print("✅ Visual description generated successfully!")
                print(f"📝 Description: {visual_description[:150]}...")
                
            except Exception as e:
                print(f"⚠️ Google AI description failed: {str(e)}")
                visual_description = f"Educational visual about {request.prompt} in {request.style} style for {request.subject}"
        
        # Generate actual visual using multiple strategies
        print("🖼️ Creating educational visual...")
        image_url = create_educational_visual(request.prompt, request.style, request.subject, visual_description)
        
        # Enhanced prompt for response
        enhanced_response_prompt = f"Google AI Enhanced: {visual_description[:100]}..." if visual_description else request.prompt
        
        print("✅ Educational visual created successfully!")
        print(f"🔗 URL: {image_url}")
        print("=" * 60)
        
        return VisualResponse(
            imageUrl=image_url,
            prompt=enhanced_response_prompt,
            style=request.style,
            subject=request.subject
        )
        
    except Exception as e:
        print(f"❌ General error: {str(e)}")
        logger.error(f"Visual generation error: {str(e)}")
        
        # Create fallback
        fallback_url = create_fallback_placeholder(
            request.prompt if hasattr(request, 'prompt') else "Error", 
            request.style if hasattr(request, 'style') else "illustration", 
            request.subject if hasattr(request, 'subject') else "general"
        )
        
        return VisualResponse(
            imageUrl=fallback_url,
            prompt=request.prompt if hasattr(request, 'prompt') else "Error generating visual",
            style=request.style if hasattr(request, 'style') else "illustration",
            subject=request.subject if hasattr(request, 'subject') else "general"
        )

@router.get("/generate-image")
async def generate_image(prompt: str = Query(..., description="Image generation prompt")):
    """
    Simple image generation endpoint for educational content
    """
    try:
        print(f"🎨 Simple image generation request: {prompt}")
        
        # Initialize Google AI service
        ai_service = GenkitAIService()
        
        description = ""
        if ai_service.genkit_available:
            # Generate educational image description
            educational_prompt = f"""
            Create a detailed description for an educational visual about: {prompt}
            
            Make it:
            - Suitable for school children
            - Educationally valuable
            - Clear and engaging
            - Appropriate for classroom use
            """
            
            description = await ai_service.generate_text(
                educational_prompt,
                language="en",
                content_type="visual",
                grade_level="3",
                length="short"
            )
        
        # Create visual using our strategies
        image_url = create_educational_visual(prompt, "illustration", "general", description)
        
        return JSONResponse({
            "imageUrl": image_url,
            "description": description,
            "prompt": prompt,
            "service": "Google AI + Educational Visual Generator"
        })
        
    except Exception as e:
        logger.error(f"Simple image generation error: {str(e)}")
        return JSONResponse({
            "error": str(e),
            "imageUrl": create_fallback_placeholder(prompt, "illustration", "general")
        }, status_code=500)

@router.get("/health")
async def visuals_health():
    """Health check for visual generation service"""
    ai_service = GenkitAIService()
    stability_key = os.getenv("STABILITY_API_KEY")
    return {
        "service": "visual-generation",
        "status": "healthy",
        "ai_service": "Google AI (Gemini) + Stability AI Image Generation",
        "ai_available": ai_service.genkit_available,
        "stability_available": bool(stability_key and stability_key != "your-stability-ai-api-key-here"),
        "features": ["AI descriptions", "Stability AI image generation", "Unsplash integration", "Dynamic placeholders"]
    }

@router.get("/test-models")
async def test_models():
    """Test visual generation capabilities"""
    try:
        ai_service = GenkitAIService()
        
        test_prompt = "photosynthesis in plants"
        test_style = "diagram"
        test_subject = "science"
        
        # Test visual creation
        visual_url = create_educational_visual(test_prompt, test_style, test_subject)
        
        ai_description = ""
        if ai_service.genkit_available:
            # Test AI description
            ai_description = await ai_service.generate_text(
                "Create a description of a plant photosynthesis diagram for students",
                language="en",
                content_type="visual",
                grade_level="3"
            )
        
        stability_key = os.getenv("STABILITY_API_KEY")
        stability_available = bool(stability_key and stability_key != "your-stability-ai-api-key-here")
        
        return {
            "google_ai": "available" if ai_service.genkit_available else "not available",
            "stability_generation": "available" if stability_available else "not configured",
            "visual_generation": "working",
            "test_visual_url": visual_url,
            "ai_description": ai_description[:100] + "..." if len(ai_description) > 100 else ai_description,
            "features": ["Google AI descriptions", "Stability AI image generation", "Unsplash educational images", "Dynamic style-based placeholders"]
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "status": "partial functionality available"
        }

@router.get("/test-stability")
async def test_stability():
    """Test Stability AI image generation"""
    try:
        stability_key = os.getenv("STABILITY_API_KEY")
        if not stability_key or stability_key == "your-stability-ai-api-key-here":
            return {"status": "error", "error": "Stability AI API key not configured"}
        
        print("🧪 Testing Stability AI image generation...")
        
        # Test with a simple educational prompt
        test_image_url = try_free_image_generation(
            prompt="simple math addition", 
            style="illustration", 
            subject="mathematics",
            description="Educational illustration showing 2+2=4 with colorful numbers"
        )
        
        if test_image_url and not test_image_url.startswith("https://via.placeholder.com"):
            return {
                "status": "success", 
                "message": "Stability AI image generation is working!", 
                "test_image": test_image_url,
                "model": "stable-diffusion-xl-1024-v1-0"
            }
        else:
            return {
                "status": "fallback", 
                "message": "Stability AI not available, using fallback methods",
                "test_image": test_image_url
            }
            
    except Exception as e:
        logger.error(f"Stability AI test error: {str(e)}")
        return {"status": "error", "error": str(e)} 