#!/usr/bin/env python3
"""
AI Setup Script for Sahayak Platform
This script helps set up and test AI capabilities
"""

import os
import sys
import asyncio
import json
from pathlib import Path

def create_env_file():
    """Create environment file with AI configuration"""
    env_content = """# AI Configuration for Sahayak Platform
# Replace these values with your actual Google Cloud credentials

# Google Cloud Settings
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Optional: OpenAI as fallback
OPENAI_API_KEY=your-openai-key

# Database
DATABASE_URL=sqlite:///sahayak.db

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Demo Mode (set to false for production)
DEMO_MODE=true
"""
    
    env_path = Path(".env")
    if not env_path.exists():
        with open(env_path, "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  Please update the .env file with your actual credentials")
    else:
        print("ℹ️  .env file already exists")

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        "google-cloud-aiplatform",
        "google-cloud-speech", 
        "vertexai",
        "fastapi",
        "uvicorn"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    else:
        print("✅ All required packages are installed")
        return True

async def test_ai_services():
    """Test AI services functionality"""
    print("\n🧪 Testing AI Services...")
    
    # Test Vertex AI Service
    try:
        from services.ollama_ai_service import OllamaAIService
        
        ai_service = OllamaAIService()
        
        # Test text generation
        response = await ai_service.generate_text(
            "Create a simple story about a cat for Grade 2 students",
            grade_level="2",
            language="en",
            content_type="story"
        )
        
        print("✅ Text generation working")
        print(f"   Sample response: {response[:100]}...")
        
        # Test image generation
        image_url = await ai_service.generate_image("A colorful educational diagram of the water cycle")
        print("✅ Image generation working")
        print(f"   Generated image URL: {image_url}")
        
    except Exception as e:
        print(f"⚠️  AI Service test failed (this is expected in demo mode): {e}")
    
    # Test Speech Service
    try:
        from services.speech_service import SpeechService
        
        speech_service = SpeechService()
        
        # Test with dummy audio data
        dummy_audio = b"dummy audio data"
        transcription = await speech_service.transcribe_audio(dummy_audio, "en-US")
        
        print("✅ Speech service working")
        print(f"   Sample transcription: {transcription}")
        
    except Exception as e:
        print(f"⚠️  Speech Service test failed (this is expected in demo mode): {e}")

def create_sample_config():
    """Create sample configuration files"""
    
    # Create logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "level": "DEBUG",
                "formatter": "default",
                "class": "logging.FileHandler",
                "filename": "sahayak.log"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["default", "file"]
        }
    }
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    with open(config_dir / "logging.json", "w") as f:
        json.dump(logging_config, f, indent=2)
    
    print("✅ Created logging configuration")

def display_next_steps():
    """Display next steps for users"""
    print("\n🎯 Next Steps to Enable AI Features:")
    print("\n1. 🌐 Set up Google Cloud:")
    print("   - Create a Google Cloud project")
    print("   - Enable Vertex AI, Speech-to-Text, and Storage APIs")
    print("   - Create a service account and download credentials JSON")
    
    print("\n2. 📝 Update Configuration:")
    print("   - Edit .env file with your Google Cloud project details")
    print("   - Set GOOGLE_APPLICATION_CREDENTIALS to your service account JSON path")
    print("   - Set DEMO_MODE=false for production")
    
    print("\n3. 🧪 Test the Setup:")
    print("   - Run: python setup_ai.py --test")
    print("   - Check all services are working correctly")
    
    print("\n4. 🚀 Deploy:")
    print("   - Start backend: uvicorn main:app --reload")
    print("   - Start frontend: npm run dev")
    
    print("\n📚 Documentation:")
    print("   - Read docs/AI_IMPLEMENTATION_GUIDE.md for detailed instructions")
    print("   - Check Google Cloud documentation for Vertex AI setup")

def main():
    """Main setup function"""
    print("🤖 Sahayak AI Setup Assistant")
    print("=" * 40)
    
    # Check if this is a test run
    if "--test" in sys.argv:
        asyncio.run(test_ai_services())
        return
    
    # Create necessary files and configs
    create_env_file()
    create_sample_config()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install missing packages before proceeding")
        return
    
    # Display next steps
    display_next_steps()
    
    print("\n✨ Setup complete! Your Sahayak platform is ready for AI integration.")
    print("🔄 Run 'python setup_ai.py --test' to test AI services.")

    print("🤖 Initializing Ollama AI service...")
    from services.ollama_ai_service import OllamaAIService
    ai_service = OllamaAIService()

    print("✅ Ollama AI service setup complete!")
    print("📍 No API keys needed - completely free!")
    print("🚀 Ready to generate unlimited educational content!")

if __name__ == "__main__":
    main() 