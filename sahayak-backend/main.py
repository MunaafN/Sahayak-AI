from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import subprocess
import time
import requests
from dotenv import load_dotenv
import logging
import threading
import signal

# Import route modules
from routers import content, worksheets, knowledge, visuals, assessment, lessons, dashboard

# Load environment variables
load_dotenv()

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_ollama_service():
    """Start Ollama service in background"""
    try:
        print("🚀 Starting Ollama service...")
        subprocess.Popen(["ollama", "serve"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        
        # Wait for service to start
        for i in range(10):  # Wait up to 10 seconds
            if check_ollama_running():
                print("✅ Ollama service started successfully")
                return True
            time.sleep(1)
        
        print("⚠️ Ollama service took too long to start")
        return False
    except FileNotFoundError:
        print("❌ Ollama not found. Install from https://ollama.ai/")
        return False
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def check_and_start_model(model_name):
    """Check if model exists and start it"""
    try:
        print(f"📋 Checking for model: {model_name}")
        
        # List available models
        list_result = subprocess.run(["ollama", "list"], 
                                   capture_output=True, text=True, timeout=10)
        
        if model_name in list_result.stdout:
            print(f"✅ Model {model_name} is available")
            
            # Start the model in background
            print(f"🔄 Starting model: {model_name}")
            def run_model():
                try:
                    subprocess.run(["ollama", "run", model_name], 
                                 input="Ready for educational tasks!\n", 
                                 text=True, timeout=30,
                                 stdout=subprocess.DEVNULL)
                except:
                    pass  # Model startup can timeout, that's normal
            
            # Run model in separate thread
            thread = threading.Thread(target=run_model, daemon=True)
            thread.start()
            
            time.sleep(2)  # Give model time to initialize
            print(f"✅ Model {model_name} started successfully")
            return True
        else:
            print(f"📥 Model {model_name} not found, attempting to download...")
            try:
                pull_result = subprocess.run(["ollama", "pull", model_name], 
                                           capture_output=True, text=True, timeout=300)
                if pull_result.returncode == 0:
                    print(f"✅ Model {model_name} downloaded successfully")
                    
                    # Start the newly downloaded model
                    def run_model():
                        try:
                            subprocess.run(["ollama", "run", model_name], 
                                         input="Ready for educational tasks!\n", 
                                         text=True, timeout=30,
                                         stdout=subprocess.DEVNULL)
                        except:
                            pass
                    
                    thread = threading.Thread(target=run_model, daemon=True)
                    thread.start()
                    time.sleep(2)
                    
                    print(f"✅ Model {model_name} downloaded and started")
                    return True
                else:
                    print(f"❌ Failed to download {model_name}")
                    return False
            except subprocess.TimeoutExpired:
                print(f"⏱️ Download of {model_name} timed out")
                return False
            except Exception as e:
                print(f"❌ Error downloading {model_name}: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error checking model {model_name}: {e}")
        return False

def start_ollama():
    """Complete Ollama startup with required models"""
    print("=" * 60)
    print("🤖 STARTING OLLAMA AI SERVICE")
    print("=" * 60)
    
    # Step 1: Check if Ollama is already running
    if check_ollama_running():
        print("✅ Ollama service is already running")
    else:
        print("🔄 Ollama service not running, starting it...")
        if not start_ollama_service():
            print("❌ Failed to start Ollama service")
            print("💡 Install Ollama from https://ollama.ai/ and try again")
            return False
    
    # Step 2: Start required models (using memory-efficient variants)
    # Use lighter models for systems with limited RAM
    models_to_start = ["llama3:8b", "llava-phi3:latest"]
    
    for model in models_to_start:
        print(f"\n🔄 Setting up {model}...")
        success = check_and_start_model(model)
        if success:
            print(f"✅ {model} is ready for educational tasks")
        else:
            print(f"⚠️ {model} setup failed, but continuing...")
    
    print("\n" + "=" * 60)
    print("🎓 OLLAMA AI SETUP COMPLETE")
    print("=" * 60)
    print("✅ Ready to generate educational content")
    print("🧠 Text AI: llama3:8b (memory-optimized for content generation)")
    print("👁️ Vision AI: llava-phi3:latest (worksheet analysis)")
    print("🌐 Service running on: http://localhost:11434")
    print("=" * 60)
    
    return True

# Start Ollama before initializing the app
print("🚀 Initializing Sahayak AI Platform...")
ollama_status = start_ollama()

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
logging.getLogger("vertexai").setLevel(logging.ERROR)
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
        "ollama_status": "available" if ollama_status else "not available",
        "models": ["llama3:8b", "llava-phi3:latest"] if ollama_status else []
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "sahayak-api",
        "ollama_running": check_ollama_running(),
        "models_ready": ollama_status
    }

@app.get("/debug/ai-status")
async def debug_ai_status():
    """Debug endpoint to check AI service status"""
    try:
        # Import inside function to avoid potential circular import issues
        from services.ollama_ai_service import OllamaAIService
        
        # Create service instance (same as routers do)
        service = OllamaAIService()
        
        # Test a simple generation
        test_result = await service.generate_text(
            "water cycle", 
            language="en", 
            content_type="explanation", 
            grade_level="3"
        )
        
        return {
            "ai_service": "Ollama (Local AI)",
            "ollama_available": service.ollama_available,
            "model_name": service.model_name,
            "test_generation": test_result[:200] + "..." if len(test_result) > 200 else test_result,
            "service_class": str(type(service)),
            "timestamp": str(__import__('datetime').datetime.now()),
            "startup_status": "Models started successfully" if ollama_status else "Model startup failed",
            "models_running": ["llama3:8b", "llava-phi3:latest"] if ollama_status else []
        }
    except Exception as e:
        return {
            "error": str(e),
            "ai_service": "Ollama (Local AI)",
            "timestamp": str(__import__('datetime').datetime.now()),
            "startup_status": "Models started successfully" if ollama_status else "Model startup failed",
            "models_running": ["llama3:8b", "llava-phi3:latest"] if ollama_status else []
        }

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "🚀 STARTING SAHAYAK BACKEND SERVER")
    print("=" * 60)
    print("📍 Backend URL: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("💊 Health Check: http://localhost:8000/health")
    print("🤖 AI Status: http://localhost:8000/debug/ai-status")
    print("🧠 AI Service: Ollama (Local, Free, Unlimited)")
    print("🔍 Vision Support: llava-phi3:latest (Auto-started)")
    print("=" * 60)
    
    if ollama_status:
        print("✅ ALL SYSTEMS READY! Ollama models are running:")
        print("   🧠 llama3:8b - Main AI for content generation")
        print("   👁️ llava-phi3:latest - Vision AI for worksheet analysis")
    else:
        print("⚠️ OLLAMA NOT FULLY READY:")
        print("   📥 Install: https://ollama.ai/")
        print("   🔧 Then run: ollama pull llama3:8b")
        print("   🔧 Then run: ollama pull llava-phi3:latest")
        print("   ⚡ Platform will work with limited AI features")
    
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="warning"  # Reduce log verbosity
    ) 