#!/usr/bin/env python3
"""
Working Sahayak Backend Server Startup
"""

import sys
import logging
import socket

def check_port_available(host, port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            return True
    except OSError:
        return False

def find_available_port(host, start_port=8000, end_port=8010):
    """Find an available port in the range"""
    for port in range(start_port, end_port + 1):
        if check_port_available(host, port):
            return port
    return None

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🚀 Starting Sahayak Backend Server...")
        
        # Import FastAPI app
        logger.info("📦 Importing application...")
        from main import app
        logger.info("✅ Application imported successfully")
        
        # Find available port
        host = "127.0.0.1"
        port = find_available_port(host, 8000, 8010)
        
        if port is None:
            logger.error("❌ No available ports found in range 8000-8010")
            sys.exit(1)
        
        logger.info(f"🌐 Using port: {port}")
        logger.info(f"📍 Server URL: http://{host}:{port}")
        logger.info(f"📚 API Docs: http://{host}:{port}/docs")
        logger.info(f"💊 Health Check: http://{host}:{port}/health")
        logger.info("-" * 60)
        
        # Start server
        import uvicorn
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            reload=False
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1) 