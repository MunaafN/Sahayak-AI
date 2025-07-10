#!/usr/bin/env python3
"""
Simple startup script for Sahayak backend
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Sahayak Backend (Simple Mode)")
    print("📍 URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🤖 AI Service: Genkit + Google Gemini (Free)")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 