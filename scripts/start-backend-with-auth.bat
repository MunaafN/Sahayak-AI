@echo off
title SAHAYAK BACKEND WITH AUTHENTICATION
echo.
echo ============================================
echo  🚀 SAHAYAK BACKEND WITH AUTHENTICATION
echo ============================================
echo.

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

echo.
echo 🔧 Backend Features:
echo    ✅ Educational Content Generation
echo    ✅ Multi-language Support (10+ Indian languages)
echo    ✅ Knowledge Base & Q&A
echo    ✅ Lesson Planning
echo    ✅ Worksheet Generation with Vision AI
echo    ✅ Reading Assessment with Speech Recognition
echo    ✅ Visual Aids Generation
echo    ✅ Google Cloud Authentication
echo    ✅ Firebase Authentication Integration
echo.
echo 🤖 AI Service: Genkit + Google Gemini
echo 🔑 Authentication: Google Cloud + Firebase
echo.

echo 🚀 Starting Sahayak Backend Server...
echo 📍 URL: http://localhost:8000
echo 🔐 Google Auth: READY
echo ============================================

python -m uvicorn main:app --reload --port 8000

pause 