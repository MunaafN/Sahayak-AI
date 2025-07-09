#!/usr/bin/env python3
"""
Simple startup script for Sahayak backend to avoid asyncio socket issues
"""
import sys
import uvicorn

def main():
    print("🚀 Starting Sahayak Backend Server (Simple Mode)...")
    print("📍 URL: http://localhost:8000")  # Using port 8000 to match main.py
    print("📚 API Docs: http://localhost:8000/docs")
    print("🤖 AI Service: Ollama (Local, Free, Unlimited)")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="localhost",
            port=8000,  # Changed to port 8000 to match frontend
            reload=False,
            access_log=False,
            log_level="warning"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Trying alternative startup method...")
        
        # Alternative method
        from main import app
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,  # Changed to port 8000
            reload=False
        )

if __name__ == "__main__":
    main() 