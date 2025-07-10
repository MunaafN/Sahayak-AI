import os
import logging
import time
import asyncio
from typing import Optional, Dict, Any
import json
from dotenv import load_dotenv

# Google AI imports (simplified - no Genkit framework)
import google.generativeai as genai

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GenkitAIService:
    """
    Simplified Google AI service - Better Hindi, enhanced prompts, no dependency conflicts
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GenkitAIService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Configuration
        self.api_key = os.getenv("GOOGLE_AI_API_KEY", "")
        self.model_name = "gemini-1.5-flash"  # Free tier model
        self.genkit_available = False
        
        # Initialize Google AI
        try:
            if self.api_key and self.api_key != "":
                # Configure Google AI
                genai.configure(api_key=self.api_key)
                
                self.genkit_available = True
                print("✅ Google AI service initialized successfully!")
                print(f"📚 Using model: {self.model_name}")
                logger.info("Google AI service initialized")
            else:
                self.genkit_available = False
                print("⚠️ Google AI API key not found. Add GOOGLE_AI_API_KEY to .env file")
                logger.warning("Google AI API key not configured")
                
        except Exception as e:
            self.genkit_available = False
            print(f"❌ Google AI initialization failed: {str(e)}")
            logger.error(f"Google AI initialization error: {str(e)}")
            
        self._initialized = True
    
    async def generate_text(self, prompt_text: str, **kwargs) -> str:
        """
        Generate educational content using Google Gemini with enhanced prompts
        """
        try:
            # Extract parameters from frontend
            language = kwargs.get("language", "en")
            content_type = kwargs.get("content_type", "explanation")
            grade_level = kwargs.get("grade_level", "3")
            subject = kwargs.get("subject", "General")
            length = kwargs.get("length", "medium")
            
            # Add timestamp to ensure fresh responses
            timestamp = int(time.time())
            
            # Map content types to actual tab/module names
            content_type_mapping = {
                "lesson_plan": "Lesson Planner",
                "explanation": "Knowledge Base", 
                "content": "Hyper Local Content Generator",
                "worksheet": "Worksheets",
                "visual": "Visual Aids",
                "assessment": "Assessment",
                "answer": "Knowledge Base",
                "story": "Content Generator",
                "example": "Content Generator",
                "activity": "Content Generator"
            }
            
            # Get the actual module name
            module_name = content_type_mapping.get(content_type, content_type.title())
            
            # Display frontend inputs in terminal
            print("=" * 60)
            print("🔥 NEW GOOGLE AI REQUEST:")
            print(f"   📋 Topic: {prompt_text}")
            print(f"   📚 Subject: {subject}")
            print(f"   🌐 Language: {language.upper()}")
            print(f"   📊 Content Type: {module_name}")
            print(f"   🎓 Grade Level: {grade_level}")
            print(f"   📏 Length: {length}")
            print(f"   🆔 Request ID: {timestamp}")
            print("=" * 60)
            
            logger.info(f"Processing: {prompt_text} | {content_type} | Grade {grade_level} | {language}")
            
            if self.genkit_available:
                try:
                    print(f"🤖 Generating content with Google Gemini...")
                    print(f"📝 Topic: {prompt_text[:50]}...")
                    print(f"🌐 Language: {language}")
                    print(f"🎯 Grade Level: {grade_level}")
                    
                    # Create educational prompt with enhanced structure
                    enhanced_prompt = self._create_educational_prompt(
                        prompt_text, language, content_type, grade_level, timestamp, length, subject
                    )
                    
                    print(f"🔍 Enhanced Prompt Preview: {enhanced_prompt[:200]}...")
                    print(f"📊 Prompt Length: {len(enhanced_prompt)} characters")
                    
                    # Generate content using Google AI directly
                    model = genai.GenerativeModel(self.model_name)
                    
                    # Configure generation parameters for better quality
                    generation_config = genai.types.GenerationConfig(
                        temperature=0.3,      # Lower for more consistent, accurate responses
                        top_p=0.95,          # High for coherent responses
                        top_k=40,            # Balanced creativity
                        max_output_tokens=800,  # Sufficient for educational content
                        candidate_count=1
                    )
                    
                    response = model.generate_content(
                        enhanced_prompt,
                        generation_config=generation_config
                    )
                    
                    if response and response.text:
                        content = response.text.strip()
                        
                        print(f"✅ Generated content successfully!")
                        print(f"📏 Response length: {len(content)} characters")
                        print(f"🔍 Response preview: {content[:100]}...")
                        print("=" * 60)
                        
                        return content
                    else:
                        error_msg = "Google AI returned empty response. Please try again."
                        print(f"⚠️ {error_msg}")
                        return self._generate_educational_fallback(prompt_text, **kwargs)
                        
                except Exception as e:
                    error_msg = f"Google AI generation error: {str(e)}"
                    print(f"❌ {error_msg}")
                    logger.error(f"Google AI API error: {str(e)}")
                    
                    # Provide helpful error message
                    if "quota" in str(e).lower():
                        error_msg = "API quota exceeded. Please try again later or check your Google AI usage."
                    elif "api_key" in str(e).lower():
                        error_msg = "API key issue. Please check your Google AI API key configuration."
                    else:
                        error_msg = f"AI service temporarily unavailable: {str(e)}"
                    
                    print(f"📤 Sending error response to frontend...")
                    return self._generate_educational_fallback(prompt_text, **kwargs)
            
            else:
                print("⚠️ Google AI not available, using educational fallback")
                fallback_response = self._generate_educational_fallback(prompt_text, **kwargs)
                print(f"📤 Fallback response: {fallback_response[:100]}...")
                return fallback_response
                
        except Exception as e:
            error_msg = "I'm sorry, I couldn't generate content at this moment. Please try again."
            logger.error(f"Error generating content: {str(e)}")
            print(f"❌ Error: {str(e)}")
            print(f"📤 Sending error response to frontend...")
            return error_msg
    
    def _create_educational_prompt(self, prompt: str, language: str, content_type: str, 
                                 grade_level: str, timestamp: int, length: str = "medium", 
                                 subject: str = "General") -> str:
        """Create educational prompt with enhanced structure"""
        
        # Define word limits clearly
        word_limits = {
            "short": {"min": 100, "max": 150},
            "medium": {"min": 200, "max": 300}, 
            "long": {"min": 400, "max": 500}
        }
        
        word_count = word_limits.get(length, word_limits["medium"])
        
        # Define grade-specific vocabulary and complexity instructions
        grade_instructions = {
            "1": "Use very simple words that a 6-7 year old can understand. Use short sentences (5-8 words). Avoid complex concepts. Use familiar examples from daily life.",
            "2": "Use simple words that a 7-8 year old can understand. Use short to medium sentences (8-12 words). Use basic concepts. Use examples from home and school.",
            "3": "Use age-appropriate words for 8-9 year olds. Use clear, medium-length sentences (10-15 words). Explain concepts step by step. Use relatable examples.",
            "4": "Use vocabulary suitable for 9-10 year olds. Use well-structured sentences (12-18 words). Include slightly more complex concepts with explanations.",
            "5": "Use vocabulary appropriate for 10-11 year olds. Use detailed sentences (15-20 words). Include more advanced concepts with clear explanations and examples."
        }
        
        grade_instruction = grade_instructions.get(grade_level, grade_instructions["3"])
        
        # Language-specific prompts with improved Hindi support
        if language == "hi":
            enhanced_prompt = f"""
आप एक अनुभवी हिंदी शिक्षक हैं। कृपया बिल्कुल शुद्ध हिंदी में लिखें।

विषय: {prompt}
कक्षा: {grade_level}
शब्द सीमा: {word_count['min']}-{word_count['max']} शब्द

महत्वपूर्ण निर्देश:
- बिल्कुल सही हिंदी व्याकरण का प्रयोग करें
- सभी तथ्य पूर्णतः सत्य और सटीक होने चाहिए
- कक्षा {grade_level} के बच्चों के लिए उपयुक्त भाषा का प्रयोग करें
- सरल और स्पष्ट वाक्यों में लिखें
- शिक्षाप्रद और रोचक शैली में लिखें

'{prompt}' के बारे में लिखें:
"""
        
        elif language == "en":
            enhanced_prompt = f"""
You are an expert educational content creator with perfect knowledge of facts and grammar.

Topic: {prompt}
Grade Level: {grade_level}  
Content Type: {content_type}
Word Limit: {word_count['min']}-{word_count['max']} words

Critical Requirements:
- Use perfect grammar and spelling
- Ensure ALL facts are completely accurate and verified
- Use simple, clear sentences appropriate for grade {grade_level} students
- Be educational, engaging, and age-appropriate
- Stay strictly within the word limit
- {grade_instruction}

Write about '{prompt}':
"""
        
        else:
            # For other languages, provide clear instructions
            enhanced_prompt = f"""
You are an educational expert. Write accurate and grammatically correct content.

Topic: {prompt}
Language: {language}
Grade Level: {grade_level}
Word Limit: {word_count['min']}-{word_count['max']} words

Requirements:
- Use correct grammar in {language}
- Ensure all facts are accurate
- Use age-appropriate language for grade {grade_level}
- Stay within word limit
- Be educational and engaging

Write about '{prompt}' in {language}:
"""
        
        return enhanced_prompt.strip()
    
    def _generate_educational_fallback(self, prompt: str, **kwargs) -> str:
        """Generate educational content when Google AI is not available"""
        language = kwargs.get("language", "en")
        grade_level = kwargs.get("grade_level", "3")
        
        fallback_messages = {
            "hi": f"""
{prompt} के बारे में:

यह एक महत्वपूर्ण विषय है जिसके बारे में कक्षा {grade_level} के छात्रों को जानना चाहिए।

कृपया Google AI API कुंजी कॉन्फ़िगर करें या बाद में पुनः प्रयास करें।

सुझाव:
• पुस्तकों से इस विषय के बारे में पढ़ें
• शिक्षकों से प्रश्न पूछें
• विश्वसनीय स्रोतों से जानकारी प्राप्त करें
""",
            "en": f"""
About {prompt}:

This is an important topic that grade {grade_level} students should understand.

Please configure Google AI API key or try again later.

Suggestions:
• Read about this topic in textbooks
• Ask your teachers questions
• Research from reliable educational sources
""",
        }
        
        return fallback_messages.get(language, f"Educational content about {prompt} will be available when Google AI API is configured.")

    async def generate_multimodal_content(self, prompt: str, image_data: str) -> str:
        """Generate content with image analysis (future feature)"""
        return "Multimodal content generation will be available in future updates."
    
    async def generate_image(self, prompt: str) -> str:
        """Generate images (not supported in free tier)"""
        return "Image generation requires premium AI services." 