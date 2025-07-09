import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting Sahayak Backend...")
    print("📍 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("💊 Health: http://localhost:8000/health")
    print("-" * 40)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 