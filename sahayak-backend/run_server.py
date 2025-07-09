#!/usr/bin/env python3
"""
Reliable server startup script for Sahayak Backend
"""

if __name__ == "__main__":
    import uvicorn
    
    # Import main app
    from main import app
    
    print("🚀 Starting Sahayak Backend Server...")
    print("📍 URL: http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    print("💊 Health Check: http://127.0.0.1:8000/health")
    print("-" * 50)
    
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        raise 