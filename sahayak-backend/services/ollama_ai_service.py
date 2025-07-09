import os
import logging
import json
import requests
import time
from typing import Optional

logger = logging.getLogger(__name__)

class OllamaAIService:
    """
    Local AI service using Ollama - Completely free with no limits!
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OllamaAIService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3:8b"  # Use memory-efficient model
        self.vision_model = "llava-phi3:latest"  # Vision model for worksheets
        self.ollama_available = self._check_ollama_availability()
        
        if self.ollama_available:
            logger.info("Ollama AI service initialized successfully")
            print("✅ Ollama AI service connected successfully!")
        else:
            logger.warning("Ollama not available. Please install Ollama and download models.")
            print("⚠️ Ollama not available. Install from https://ollama.ai/")
            
        self._initialized = True
    
    def _check_ollama_availability(self):
        """Check if Ollama is running and has models available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    # Check for memory-efficient models first
                    model_names = [model['name'] for model in models]
                    
                    # First priority: llama3:8b (memory-efficient)
                    if "llama3:8b" in model_names:
                        self.model_name = "llama3:8b"
                        print(f"📚 Using text AI model: {self.model_name}")
                        
                        # Check for vision model
                        if "llava-phi3:latest" in model_names:
                            print(f"👁️ Using vision AI model: {self.vision_model}")
                        else:
                            print("⚠️ llava-phi3:latest not found for vision features")
                        
                        return True
                    
                    # Fallback to llama3:latest (also memory-efficient)
                    elif "llama3:latest" in model_names:
                        self.model_name = "llama3:latest"
                        print(f"📚 Using fallback text model: {self.model_name}")
                        return True
                    
                    # Fallback to any llama3.1 variant
                    elif any("llama3.1" in name for name in model_names):
                        for name in model_names:
                            if "llama3.1" in name:
                                self.model_name = name
                                break
                        print(f"📚 Using fallback text model: {self.model_name}")
                        print("⚠️ This model may require more memory")
                        return True
                    
                    # Fallback to any llama3 variant  
                    elif any("llama3" in name for name in model_names):
                        for name in model_names:
                            if "llama3" in name:
                                self.model_name = name
                                break
                        print(f"📚 Using fallback model: {self.model_name}")
                        return True
                    
                    # Last resort: any llama model
                    elif any("llama" in name for name in model_names):
                        for name in model_names:
                            if "llama" in name:
                                self.model_name = name
                                break
                        print(f"📚 Using available model: {self.model_name}")
                        return True
                    
                    else:
                        # Use first available model
                        self.model_name = model_names[0]
                        print(f"📚 Using available model: {self.model_name}")
                        return True
                else:
                    print("⚠️ No models found. Run: ollama pull llama3:8b")
                    return False
            return False
        except Exception as e:
            logger.debug(f"Ollama check failed: {e}")
            return False
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate educational content using local Ollama AI
        
        Args:
            prompt: Text prompt for generation
            **kwargs: Additional parameters (language, content_type, grade_level)
            
        Returns:
            Generated educational content
        """
        try:
            # Add timestamp to ensure fresh responses
            timestamp = int(time.time())
            
            # Extract parameters from frontend
            language = kwargs.get("language", "en")
            content_type = kwargs.get("content_type", "explanation")
            grade_level = kwargs.get("grade_level", "3")
            subject = kwargs.get("subject", "General")
            length = kwargs.get("length", "medium")  # Extract length parameter
            
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
            print("📝 NEW REQUEST FROM FRONTEND:")
            print(f"   📋 Topic: {prompt}")
            print(f"   📚 Subject: {subject}")
            print(f"   🌐 Language: {language.upper()}")
            print(f"   📊 Content Type: {module_name}")
            print(f"   🎓 Grade Level: {grade_level}")
            print(f"   🆔 Request ID: {timestamp}")
            print("=" * 60)
            
            logger.info(f"Processing: {prompt} | {content_type} | Grade {grade_level} | {language}")
            
            if self.ollama_available:
                try:
                    if self._check_ollama_availability():
                        print(f"🤖 Generating content with Ollama...")
                        print(f"📝 Prompt Topic: {prompt[:50]}...")
                        print(f"🌐 Language: {language}")
                        print(f"🎯 Grade Level: {grade_level}")
                        print(f"📏 Length: {length}")
                        print(f"📚 Content Type: {content_type}")
                        
                        # Create educational prompt with strict language enforcement
                        enhanced_prompt = self._create_educational_prompt(prompt, language, content_type, grade_level, timestamp, length, subject)
                        
                        print(f"🔍 Enhanced Prompt Preview: {enhanced_prompt[:200]}...")
                        print(f"📊 Prompt Length: {len(enhanced_prompt)} characters")
                        
                        try:
                            response = requests.post(
                                f"{self.ollama_url}/api/generate",
                                json={
                                    "model": self.model_name,
                                    "prompt": enhanced_prompt,
                                    "stream": False,
                                    "options": {
                                        "temperature": 0.7,
                                        "top_p": 0.9,
                                        "num_predict": 500
                                    }
                                },
                                timeout=60
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                content = result.get('response', '').strip()
                                
                                print(f"✅ Generated content successfully")
                                print(f"📏 Response length: {len(content)} characters")
                                print(f"🔍 Response preview: {content[:100]}...")
                                
                                return content
                            
                            elif response.status_code == 500:
                                # Handle HTTP 500 errors with detailed feedback
                                error_text = response.text.lower()
                                print(f"❌ HTTP 500 Error from Ollama")
                                print(f"🔍 Error text: {error_text[:200]}...")
                                
                                try:
                                    error_json = response.json()
                                    error_msg = error_json.get('error', error_text)
                                    print(f"📄 Error details: {error_msg}")
                                    
                                    # Check for memory-related errors
                                    if any(term in error_text for term in ['memory', 'insufficient', 'oom', 'out of memory', 'allocation failed']):
                                        error_msg = "Insufficient memory to run AI model. Try restarting Ollama or closing other applications."
                                        print(f"🧠 Memory Error: {error_text}")
                                        print(f"💡 Try: ollama serve --host 0.0.0.0 --origin \"*\"")
                                    else:
                                        error_msg = f"AI model error: {error_text[:100]}..."
                                        print(f"❌ Model Error: {error_text}")
                                except:
                                    error_msg = "AI model is not responding properly. Please restart Ollama service."
                                    print(f"❌ HTTP 500: Model not loaded properly")
                                
                                print(f"💡 Suggestion: Stop Ollama, restart it, and try again")
                                print(f"📤 Sending error response to frontend...")
                                return error_msg
                            else:
                                error_msg = f"AI service error: HTTP {response.status_code}"
                                print(f"❌ {error_msg}")
                                
                                # Try to get error details
                                try:
                                    error_details = response.json()
                                    print(f"🔍 Error details: {error_details}")
                                except:
                                    print(f"🔍 Raw response: {response.text[:200]}...")
                                
                                return error_msg
                                
                        except requests.exceptions.Timeout:
                            error_msg = "The AI is taking too long to respond. Please try again."
                            print(f"⏱️ {error_msg}")
                            return error_msg
                        except Exception as e:
                            error_msg = f"AI service error: {str(e)}"
                            logger.error(f"Ollama API error: {str(e)}")
                            print(f"❌ {error_msg}")
                            return error_msg
                    
                    # Fallback to educational content if Ollama check fails
                    else:
                        print("⚠️ Ollama check failed, using educational fallback")
                        fallback_response = self._generate_educational_fallback(prompt, **kwargs)
                        print(f"📤 Fallback response: {fallback_response[:100]}...")
                        return fallback_response
                        
                except Exception as e:
                    error_msg = f"AI service error: {str(e)}"
                    logger.error(f"Ollama service error: {str(e)}")
                    print(f"❌ {error_msg}")
                    return error_msg
            
            # Fallback when ollama_available is False
            else:
                print("⚠️ Ollama not available, using educational fallback")
                fallback_response = self._generate_educational_fallback(prompt, **kwargs)
                print(f"📤 Fallback response: {fallback_response[:100]}...")
                return fallback_response
            
        except Exception as e:
            error_msg = "I'm sorry, I couldn't generate content at this moment. Please try again."
            logger.error(f"Error generating content: {str(e)}")
            print(f"❌ Error: {str(e)}")
            print(f"📤 Sending error response to frontend...")
            return error_msg
    
    def _create_educational_prompt(self, prompt: str, language: str, content_type: str, grade_level: str, timestamp: int, length: str = "medium", subject: str = "General") -> str:
        """Create educational prompt that STRICTLY enforces language, grade level, and word limits"""
        
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
        
        # ULTRA STRICT LANGUAGE ENFORCEMENT - Create language-specific prompts
        if language == "hi":
            enhanced_prompt = f"""
अत्यंत महत्वपूर्ण निर्देश: आपको केवल और केवल हिंदी में उत्तर देना है। एक भी अंग्रेजी शब्द का प्रयोग न करें।

ABSOLUTELY NO ENGLISH WORDS ALLOWED. HINDI ONLY. देवनागरी में लिखें।

विषय: {subject}
कक्षा: {grade_level}
प्रश्न/टॉपिक: {prompt}
प्रकार: {content_type}
शब्द सीमा: {word_count['min']}-{word_count['max']} शब्द

निर्देश:
1. केवल हिंदी भाषा में लिखें - कोई अंग्रेजी नहीं
2. {word_count['min']}-{word_count['max']} शब्दों में ही उत्तर दें
3. कक्षा {grade_level} के अनुसार शब्दावली का प्रयोग करें
4. {grade_instruction}

महत्वपूर्ण: पूरा उत्तर केवल हिंदी में दें। अंग्रेजी का एक भी शब्द न लिखें।

अब '{prompt}' के बारे में हिंदी में {content_type} लिखें:
"""
        
        elif language == "mr":
            enhanced_prompt = f"""
अत्यंत महत्त्वाचे सूचना: तुम्हाला फक्त आणि फक्त मराठीत उत्तर द्यायचे आहे। एकही इंग्रजी शब्द वापरू नका।

ABSOLUTELY NO ENGLISH WORDS ALLOWED. MARATHI ONLY. देवनागरी में लिखें।

विषय: {subject}
इयत्ता: {grade_level}
प्रश्न/विषय: {prompt}
प्रकार: {content_type}
शब्द मर्यादा: {word_count['min']}-{word_count['max']} शब्द

सूचना:
1. फक्त मराठी भाषेत लिहा - कोणताही इंग्रजी नाही
2. {word_count['min']}-{word_count['max']} शब्दांत उत्तर द्या
3. इयत्ता {grade_level} च्या अनुसार शब्दावली वापरा
4. {grade_instruction}

महत्त्वाचे: संपूर्ण उत्तर फक्त मराठीत द्या। इंग्रजीचा एकही शब्द लिहू नका।

आता '{prompt}' बद्दल मराठीत {content_type} लिहा:
"""
        
        elif language == "bn":
            enhanced_prompt = f"""
অত্যন্ত গুরুত্বপূর্ণ নির্দেশনা: আপনাকে কেবলমাত্র বাংলায় উত্তর দিতে হবে। একটি ইংরেজি শব্দও ব্যবহার করবেন না।

ABSOLUTELY NO ENGLISH WORDS ALLOWED. BENGALI ONLY. বাংলায় লিখুন।

বিষয়: {subject}
শ্রেণী: {grade_level}
প্রশ্ন/বিষয়: {prompt}
ধরন: {content_type}
শব্দ সীমা: {word_count['min']}-{word_count['max']} শব্দ

নির্দেশনা:
1. কেবল বাংলা ভাষায় লিখুন - কোন ইংরেজি নয়
2. {word_count['min']}-{word_count['max']} শব্দে উত্তর দিন
3. শ্রেণী {grade_level} অনুযায়ী শব্দভাণ্ডার ব্যবহার করুন
4. {grade_instruction}

গুরুত্বপূর্ণ: সম্পূর্ণ উত্তর কেবল বাংলায় দিন। ইংরেজির একটি শব্দও লিখবেন না।

এখন '{prompt}' সম্পর্কে বাংলায় {content_type} লিখুন:
"""
        
        elif language == "te":
            enhanced_prompt = f"""
అత్యంత ముఖ్యమాన సూచనలు: మీరు కేవలం తెలుగులో మాత్రమే సమాధానం ఇవ్వాలి. ఒక్క ఇంగ్లీష్ పదం కూడా వాడకండి.

ABSOLUTELY NO ENGLISH WORDS ALLOWED. TELUGU ONLY. తెలుగులో రాయండి.

విషయం: {subject}
తరగతి: {grade_level}
ప్రశ్న/విషయం: {prompt}
రకం: {content_type}
పదాల పరిమితి: {word_count['min']}-{word_count['max']} పదాలు

సూచనలు:
1. కేవలం తెలుగు భాషలో రాయండి - ఇంగ్లీష్ వద్దు
2. {word_count['min']}-{word_count['max']} పదాలలో సమాధానం ఇవ్వండి
3. తరగతి {grade_level} అనుసారం పదజాలం వాడండి
4. {grade_instruction}

ముఖ్యం: మొత్తం సమాధానం కేవలం తెలుగులో ఇవ్వండి. ఇంగ్లీష్ పదం రాయకండి.

ఇప్పుడు '{prompt}' గురించి తెలుగులో {content_type} రాయండి:
"""
        
        elif language == "ta":
            enhanced_prompt = f"""
மிக முக்கியமான அறிவுறுத்தல்கள்: நீங்கள் தமிழில் மட்டுமே பதிலளிக்க வேண்டும். ஒரு ஆங்கில வார்த்தையும் பயன்படுத்த வேண்டாம்.

ABSOLUTELY NO ENGLISH WORDS ALLOWED. TAMIL ONLY. தமிழில் எழுதுங்கள்.

பாடம்: {subject}
வகுப்பு: {grade_level}
கேள்வி/தலைப்பு: {prompt}
வகை: {content_type}
வார்த்தை வரம்பு: {word_count['min']}-{word_count['max']} வார்த்தைகள்

அறிவுறுத்தல்கள்:
1. தமிழ் மொழியில் மட்டுமே எழுதுங்கள் - ஆங்கிலம் வேண்டாம்
2. {word_count['min']}-{word_count['max']} வார்த்தைகளில் பதிலளியுங்கள்
3. வகுப்பு {grade_level} அளவுக்கு ஏற்ற சொற்கள் பயன்படுத்துங்கள்
4. {grade_instruction}

முக்கியம்: முழு பதிலும் தமிழில் மட்டுமே தருங்கள். ஆங்கில வார்த்தை எழுத வேண்டாம்.

இப்போது '{prompt}' பற்றி தமிழில் {content_type} எழுதுங்கள்:
"""
        
        elif language == "gu":
            enhanced_prompt = f"""
અત્યંત મહત્વપૂર્ણ સૂચનાઓ: તમારે ફક્ત ગુજરાતીમાં જ જવાબ આપવાનો છે. એક પણ અંગ્રેજી શબ્દ વાપરશો નહીં.

ABSOLUTELY NO ENGLISH WORDS ALLOWED. GUJARATI ONLY. ગુજરાતીમાં લખો.

વિષય: {subject}
ધોરણ: {grade_level}
પ્રશ્ન/વિષય: {prompt}
પ્રકાર: {content_type}
શબ્દ મર્યાદા: {word_count['min']}-{word_count['max']} શબ્દો

સૂચનાઓ:
1. ફક્ત ગુજરાતી ભાષામાં લખો - અંગ્રેજી નહીં
2. {word_count['min']}-{word_count['max']} શબ્દોમાં જવાબ આપો
3. ધોરણ {grade_level} અનુસાર શબ્દભંડોળ વાપરો
4. {grade_instruction}

મહત્વપૂર્ણ: સંપૂર્ણ જવાબ ફક્ત ગુજરાતીમાં આપો. અંગ્રેજીનો એક પણ શબ્દ લખશો નહીં.

હવે '{prompt}' વિશે ગુજરાતીમાં {content_type} લખો:
"""
        
        else:
            # For English and any other language, use very strict instructions
            enhanced_prompt = f"""
🚨 ULTRA CRITICAL LANGUAGE ENFORCEMENT 🚨
LANGUAGE: {language.upper()} ONLY
ABSOLUTELY NO ENGLISH OR OTHER LANGUAGES ALLOWED!

You MUST respond ONLY in {language.upper()} language. Do NOT use English or any other language.

Subject: {subject}
Grade: {grade_level}
Topic: {prompt}
Type: {content_type}
Word limit: {word_count['min']}-{word_count['max']} words EXACTLY

STRICT REQUIREMENTS:
1. Language: {language.upper()} ONLY (zero English words allowed)
2. Word count: {word_count['min']}-{word_count['max']} words (count each word carefully)
3. Grade {grade_level} appropriate vocabulary and concepts
4. {grade_instruction}

🚨 CRITICAL: Your entire response must be in {language.upper()} language. Count words carefully and stay within {word_count['min']}-{word_count['max']} words limit.

Now write {content_type} about '{prompt}' in {language.upper()} language:
"""
        
        return enhanced_prompt.strip()
    
    def _generate_educational_fallback(self, prompt: str, **kwargs) -> str:
        """Generate educational content when Ollama is not available"""
        language = kwargs.get("language", "en")
        grade_level = kwargs.get("grade_level", "3")
        
        fallback_messages = {
            "hi": f"""
{prompt} के बारे में:

यह एक बहुत अच्छा सवाल है! जब Ollama AI उपलब्ध नहीं है, तो हम आपको सुझाव देते हैं:

• पुस्तकों से पढ़ें
• शिक्षकों से पूछें  
• इंटरनेट पर खोजें

कृपया Ollama स्थापित करें और एक मॉडल डाउनलोड करें ताकि आपको बेहतर उत्तर मिल सकें।

सीखते रहें!
""",
            "mr": f"""
{prompt} बद्दल:

हा एक छान प्रश्न आहे! जेव्हा Ollama AI उपलब्ध नाही, तेव्हा आम्ही सुचवतो:

• पुस्तकांमधून वाचा
• शिक्षकांना विचारा
• इंटरनेटवर शोधा

कृपया Ollama स्थापित करा आणि मॉडेल डाउनलोड करा जेणेकरून तुम्हाला चांगली उत्तरे मिळतील।

शिकत राहा!
""",
            "bn": f"""
{prompt} সম্পর্কে:

এটি একটি দুর্দান্ত প্রশ্ন! যখন Ollama AI উপলব্ধ নেই, তখন আমরা সুপারিশ করি:

• বই থেকে পড়ুন
• শিক্ষকদের জিজ্ঞাসা করুন
• ইন্টারনেটে অনুসন্ধান করুন

দয়া করে Ollama ইনস্টল করুন এবং একটি মডেল ডাউনলোড করুন যাতে আপনি আরও ভাল উত্তর পেতে পারেন।

শেখা চালিয়ে যান!
""",
            "te": f"""
{prompt} గురించి:

ఇది చాలా మంచి ప్రశ్న! Ollama AI అందుబాటులో లేనప్పుడు, మేము సూచిస్తున్నాము:

• పుస్తకాల నుండి చదవండి
• ఉపాధ్యాయులను అడగండి
• ఇంటర్నెట్లో వెతకండి

దయచేసి Ollama ఇన్స్టాల్ చేసి, మాడల్ డౌన్లోడ్ చేయండి, తద్వారా మీకు మెరుగైన సమాధానాలు లభిస్తాయి।

నేర్చుకోవడం కొనసాగించండి!
""",
            "ta": f"""
{prompt} பற்றி:

இது ஒரு சிறந்த கேள்வி! Ollama AI கிடைக்காதபோது, நாங்கள் பரிந்துரைக்கிறோம்:

• புத்தகங்களில் இருந்து படியுங்கள்
• ஆசிரியர்களிடம் கேளுங்கள்
• இணையத்தில் தேடுங்கள்

தயவுசெய்து Ollama நிறுவி மாடலை பதிவிறக்கம் செய்யுங்கள், இதனால் சிறந்த பதில்கள் கிடைக்கும்।

கற்றுக்கொண்டே இருங்கள்!
""",
            "gu": f"""
{prompt} વિશે:

આ એક ખૂબ સારો પ્રશ્ન છે! જ્યારે Ollama AI ઉપલબ્ધ ન હોય, અમે સૂચવીએ છીએ:

• પుસ્તકોમાંથી વાંચો
• શિક્ષકોને પૂછો
• ઇન્ટરનેટ પર શોધો

કૃપા કરીને Ollama ઇન્સ્ટોલ કરો અને મોડൽ ડൗൺલോડ કરો જેથી તમને વધુ સારા જવાબો મળે।

શીખતા રહો!
""",
            "kn": f"""
{prompt} ಬಗ್ಗೆ:

ಇದು ಒಂದು ಉತ್ತಮ ಪ್ರಶ್ನೆ! Ollama AI ಲಭ್ಯವಿಲ್ಲದಿದ್ದಾಗ, ನಾವು ಸೂಚಿಸುತ್ತೇವೆ:

• ಪುಸ್ತಕಗಳಿಂದ ಓದಿ
• ಶಿಕ್ಷಕರನ್ನು ಕೇಳಿ
• ಇಂಟರ್ನെಟ್‌ನಲ್ಲಿ ಹುಡುಕಿ

ದಯವಿಟ್ಟು Ollama ಸ್ಥಾಪಿಸಿ ಮತ್ತು ಮಾಡೆಲ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ ಇದರಿಂದ ನಿಮಗೆ ಉತ್ತಮ ಉತ್ತರಗಳು ಸಿಗುತ್ತವೆ।

ಕಲಿಯುತ್ತಾ ಇರಿ!
""",
            "ml": f"""
{prompt} കുറിച്ച്:

ഇത് ഒരു നല്ല ചോദ്യമാണ്! Ollama AI ലഭ്യമല്ലാത്തപ്പോൾ, ഞങ്ങൾ നിർദ്ദേശിക്കുന്നു:

• പുസ്തകങ്ങളിൽ നിന്ന് വായിക്കുക
• അധ്യാപകരോട് ചോദിക്കുക
• ഇന്റർനെറ്റിൽ തിരയുക

ദയവായി Ollama ഇൻസ്റ്റാൾ ചെയ്ത് മോഡൽ ഡൗൺലോഡ് ചെയ്യുക, അങ്ങനെ നിങ്ങൾക്ക് മികച്ച ഉത്തരങ്ങൾ ലഭിക്കും।

പഠിക്കുന്നത് തുടരുക!
""",
            "ur": f"""
{prompt} کے بارے میں:

یہ ایک بہترین سوال ہے! جب Ollama AI دستیاب نہیں ہے تو ہم تجویز کرتے ہیں:

• کتابوں سے پڑھیں
• اساتذہ سے پوچھیں
• انٹرنیٹ پر تلاش کریں

برائے کرم Ollama انسٹال کریں اور ماڈل ڈاؤن لوڈ کریں تاکہ آپ کو بہتر جوابات مل سکیں۔

سیکھتے رہیں!
"""
        }
        
        if language in fallback_messages:
            return fallback_messages[language]
        else:
            return f"""
About "{prompt}":

That's a great question! When Ollama AI is not available, we suggest:

• Read books about this topic
• Ask your teachers
• Search on the internet for reliable sources

Please install Ollama and download a model to get better AI-generated answers.

Keep learning!
"""

    # Keep compatibility with existing multimodal methods
    async def generate_multimodal_content(self, prompt: str, image_data: str) -> str:
        return "Multimodal content generation not implemented with Ollama yet."
    
    async def generate_image(self, prompt: str) -> str:
        return "Image generation not implemented with Ollama yet." 