#!/usr/bin/env python3
"""
Robust startup script for Sahayak backend with error handling and dependency checks
"""
import sys
import os
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("🔄 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_genkit():
    """Check if Genkit AI is available"""
    try:
        # Check if Google AI API key is configured
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_AI_API_KEY", "")
        if api_key and api_key != "":
            print("✅ Genkit AI service is configured and ready!")
            print("🔑 Google AI API key found")
            return True
        else:
            print("⚠️ Google AI API key not configured")
            print("💡 Add GOOGLE_AI_API_KEY to .env file")
            return False
    except Exception as e:
        print("⚠️ Genkit AI service not available")
        print("💡 Please configure Google AI API key:")
        print("   - Get key from: https://ai.google.dev/")
        print("   - Add to .env: GOOGLE_AI_API_KEY=your_key_here")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Sahayak Backend Server...")
    print("📍 URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🤖 AI Service: Genkit + Google Gemini")
    print("-" * 50)
    
    try:
        import uvicorn
        from main import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False
        )
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Installing missing dependencies...")
        install_dependencies()
        # Try again
        import uvicorn
        from main import app
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main startup routine"""
    print("🎯 Sahayak Backend Startup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check current directory
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Please run this script from the sahayak-backend directory.")
        sys.exit(1)
    
    # Install dependencies if needed
    if not os.path.exists("requirements.txt"):
        print("⚠️ requirements.txt not found")
    else:
        install_dependencies()
    
    # Check Genkit AI
    check_genkit()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main() 