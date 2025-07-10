from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import time
from dotenv import load_dotenv
import logging

# Import route modules
from routers import content, worksheets, knowledge, visuals, assessment, lessons, dashboard

# Load environment variables
load_dotenv()

def check_google_ai_setup():
    """Check if Google AI is properly configured"""
    try:
        api_key = os.getenv("GOOGLE_AI_API_KEY")
        if not api_key:
            print("❌ GOOGLE_AI_API_KEY not found in environment variables")
            return False
        
        if api_key.startswith("AIza") and len(api_key) == 39:
            print("✅ Google AI API key format is valid")
            return True
        else:
            print("⚠️ Google AI API key format seems incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Google AI setup: {e}")
        return False

def test_google_ai_connection():
    """Test Google AI service connection"""
    try:
        print("🔄 Testing Google AI connection...")
        
        # Import and test the service
        from services.genkit_ai_service import GenkitAIService
        service = GenkitAIService()
        
        # Check if the service is properly configured
        if service.genkit_available and service.api_key:
            print("✅ Google AI service initialized successfully")
            return True
        else:
            print("⚠️ Google AI service initialization had issues")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import Google AI service: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing Google AI connection: {e}")
        return False

def start_google_ai():
    """Initialize Google AI service"""
    print("=" * 60)
    print("🤖 STARTING GOOGLE AI SERVICE")
    print("=" * 60)
    
    # Step 1: Check API key configuration
    if not check_google_ai_setup():
        print("❌ Google AI setup failed")
        print("💡 Please set GOOGLE_AI_API_KEY in your .env file")
        print("📝 Get your API key from: https://ai.google.dev/")
        return False
    
    # Step 2: Test service connection
    if not test_google_ai_connection():
        print("❌ Google AI connection test failed")
        return False
    
    print("\n" + "=" * 60)
    print("🎓 GOOGLE AI SETUP COMPLETE")
    print("=" * 60)
    print("✅ Ready to generate educational content")
    print("🧠 AI Model: Google Gemini (Cloud-based, High Quality)")
    print("🌏 Hindi Language: Optimized for Indian education")
    print("🌐 Service: Google AI Platform")
    print("=" * 60)
    
    return True

# Start Google AI before initializing the app
print("🚀 Initializing Sahayak AI Platform...")
ai_status = start_google_ai()

# Initialize FastAPI app
app = FastAPI(
    title="Sahayak API",
    description="AI-powered teaching assistant for multi-grade classrooms",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging with less verbose output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Reduce logging from external libraries
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Create uploads directory for generated visuals
os.makedirs("uploads/visuals", exist_ok=True)

# Mount static files for serving generated images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers without /api prefix to match frontend expectations
app.include_router(content.router, prefix="/content", tags=["content"])
app.include_router(worksheets.router, prefix="/worksheets", tags=["worksheets"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
app.include_router(visuals.router, prefix="/visuals", tags=["visuals"])
app.include_router(assessment.router, prefix="/assessment", tags=["assessment"])
app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Sahayak API",
        "description": "AI-powered teaching assistant for multi-grade classrooms",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running in educational mode",
        "ai_service": "Google AI (Gemini)",
        "ai_status": "available" if ai_status else "not available",
        "features": ["content generation", "Hindi support", "visual analysis", "assessments"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "sahayak-api",
        "ai_service": "Google AI",
        "ai_ready": ai_status,
        "google_ai_configured": check_google_ai_setup()
    }

@app.get("/debug/ai-status")
async def debug_ai_status():
    """Debug endpoint to check AI service status"""
    try:
        # Import inside function to avoid potential circular import issues
        from services.genkit_ai_service import GenkitAIService
        
        # Create service instance (same as routers do)
        service = GenkitAIService()
        
        # Test a simple generation
        test_result = await service.generate_text(
            "water cycle", 
            language="en", 
            content_type="explanation", 
            grade_level="3"
        )
        
        return {
            "ai_service": "Google AI (Gemini)",
            "service_available": True,
            "model_name": getattr(service, 'model_name', 'gemini-1.5-flash'),
            "test_generation": test_result[:200] + "..." if len(test_result) > 200 else test_result,
            "service_class": str(type(service)),
            "timestamp": str(__import__('datetime').datetime.now()),
            "startup_status": "Google AI started successfully" if ai_status else "Google AI startup failed",
            "api_key_configured": bool(os.getenv("GOOGLE_AI_API_KEY"))
        }
    except Exception as e:
        return {
            "error": str(e),
            "ai_service": "Google AI (Gemini)",
            "service_available": False,
            "timestamp": str(__import__('datetime').datetime.now()),
            "startup_status": "Google AI started successfully" if ai_status else "Google AI startup failed",
            "api_key_configured": bool(os.getenv("GOOGLE_AI_API_KEY"))
        }

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "🚀 STARTING SAHAYAK BACKEND SERVER")
    print("=" * 60)
    print("📍 Backend URL: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("💊 Health Check: http://localhost:8000/health")
    print("🤖 AI Status: http://localhost:8000/debug/ai-status")
    print("🧠 AI Service: Google AI (Gemini)")
    print("🌏 Language Support: Hindi + English optimized")
    print("=" * 60)
    
    if ai_status:
        print("✅ ALL SYSTEMS READY! Google AI is configured:")
        print("   🧠 Google Gemini - High-quality content generation")
        print("   🌏 Hindi Language - Optimized for Indian education")
        print("   ☁️ Cloud-based - No local model downloads needed")
    else:
        print("⚠️ GOOGLE AI NOT READY:")
        print("   🔑 Set GOOGLE_AI_API_KEY in .env file")
        print("   🌐 Get API key: https://ai.google.dev/")
        print("   ⚡ Platform will work with limited AI features")
    
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="warning"  # Reduce log verbosity
    ) 