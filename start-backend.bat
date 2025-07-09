@echo off
echo.
echo ================================
echo   🚀 Starting Sahayak Backend
echo ================================
echo.
echo 📍 Backend URL: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 💊 Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ================================
echo.

cd /d "%~dp0sahayak-backend"
python main.py

pause 