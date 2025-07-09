@echo off
echo ================================
echo SAHAYAK BACKEND - GOOGLE AUTH READY
echo ================================

REM Change to backend directory
cd /d "%~dp0..\sahayak-backend"

echo 🔍 Checking Google Cloud Authentication Setup...

REM Check if Google Cloud credentials file exists
if not exist "sahayak-credentials.json" (
    echo ❌ Google Cloud credentials file not found!
    echo 📄 Expected: sahayak-credentials.json
    echo 💡 Please ensure your Google Cloud service account credentials are in place
    pause
    exit /b 1
)

echo ✅ Google Cloud credentials file found

REM Set Google Application Credentials environment variable
set GOOGLE_APPLICATION_CREDENTIALS=%CD%\sahayak-credentials.json
echo ✅ Google Application Credentials set: %GOOGLE_APPLICATION_CREDENTIALS%

REM Check if .env file exists
if not exist ".env" (
    echo 📋 Creating backend environment configuration...
    copy "..\config\backend-env-actual.txt" ".env"
    if exist ".env" (
        echo ✅ Backend .env file created
    ) else (
        echo ⚠️ Could not create .env file automatically
    )
) else (
    echo ✅ Backend .env file exists
)

REM Check frontend .env file
echo 🔍 Checking Frontend Authentication Setup...
if not exist "..\sahayak-frontend\.env" (
    echo 📋 Creating frontend environment configuration...
    copy "..\config\frontend-env-actual.txt" "..\sahayak-frontend\.env"
    if exist "..\sahayak-frontend\.env" (
        echo ✅ Frontend .env file created
    ) else (
        echo ⚠️ Could not create frontend .env file automatically
    )
) else (
    echo ✅ Frontend .env file exists
)

echo.
echo 🔍 Checking Python Virtual Environment...
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found - using system Python
)

echo.
echo 🔍 Checking Required AI Models...
echo 📥 Starting llava-phi3 model for vision-based worksheets...
start /min cmd /c "ollama run llava-phi3 & exit"

echo ⏳ Waiting for vision model to initialize...
timeout /t 3 /nobreak >nul

echo.
echo 🚀 Starting Sahayak Backend Server...
echo 📍 URL: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🔐 Google Auth: READY
echo 🤖 AI Service: Ollama (Local)
echo 🔍 Vision Worksheets: llava-phi3
echo ☁️ Google Cloud: Configured
echo ================================

python main.py

echo.
echo 🔄 Backend server stopped
pause 