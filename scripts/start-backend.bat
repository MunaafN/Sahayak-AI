@echo off
echo ================================
echo SAHAYAK BACKEND - WITH GOOGLE AUTH
echo ================================

cd sahayak-backend

echo 🔍 Checking Google Cloud Authentication...
if not exist "sahayak-credentials.json" (
    echo ❌ Google Cloud credentials missing!
    echo 💡 Please ensure sahayak-credentials.json is in the backend directory
    pause
    exit /b 1
)

echo ✅ Google Cloud credentials found
set GOOGLE_APPLICATION_CREDENTIALS=%CD%\sahayak-credentials.json

echo 🔍 Checking Environment Configuration...
if not exist ".env" (
    echo 📋 Creating backend .env file...
    copy "..\config\backend-env-actual.txt" ".env"
)

echo 🔍 Checking Frontend Authentication...
if not exist "..\sahayak-frontend\.env" (
    echo 📋 Creating frontend .env file...
    copy "..\config\frontend-env-actual.txt" "..\sahayak-frontend\.env"
)

echo 🐍 Activating Virtual Environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
) else (
    echo ⚠️ Virtual environment not found - using system Python
)

echo 🤖 Starting AI Models...
echo 📥 Initializing llava-phi3 for vision-based worksheets...
start /min cmd /c "ollama run llava-phi3 & exit"

echo ⏳ Waiting for model initialization...
timeout /t 2 /nobreak >nul

echo 🚀 Starting Sahayak Backend Server...
echo 📍 URL: http://localhost:8000
echo 🔐 Google Auth: READY
echo ================================

python -m uvicorn main:app --reload --port 8000
pause
