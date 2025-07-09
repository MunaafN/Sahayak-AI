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

def check_ollama():
    """Check if Ollama is available"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print(f"✅ Ollama is running with {len(models)} model(s)")
                for model in models:
                    print(f"   📚 Model: {model['name']}")
                return True
            else:
                print("⚠️ Ollama is running but no models found")
                print("💡 Run: ollama pull llama3.1:8b")
                return False
        else:
            print("⚠️ Ollama is not responding properly")
            return False
    except Exception as e:
        print("⚠️ Ollama is not running")
        print("💡 Please start Ollama first:")
        print("   - Windows: Run Ollama.exe")
        print("   - Then run: ollama pull llama3.1:8b")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Sahayak Backend Server...")
    print("📍 URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🤖 AI Service: Ollama (Local)")
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
    
    # Check Ollama
    check_ollama()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main() 