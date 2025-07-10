@echo off
title SAHAYAK BACKEND SERVER STARTUP
echo.
echo ============================================
echo  🚀 SAHAYAK BACKEND SERVER STARTUP
echo ============================================
echo.

echo 📋 Step 1: Environment Check
echo.

REM Check if we're in the correct directory
if not exist "main.py" (
    echo ❌ main.py not found!
    echo Please run this script from sahayak-backend directory
    echo.
    pause
    exit /b 1
)

echo ✅ Found main.py - we're in the right directory

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ No virtual environment found - using global Python
)

echo.
echo 📋 Step 2: Installing Dependencies
echo.

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

echo.
echo 📋 Step 3: Starting Backend Server
echo.

echo 🔧 Backend Features:
echo    ✅ Educational Content Generation
echo    ✅ Multi-language Support (10+ Indian languages)
echo    ✅ Knowledge Base & Q&A
echo    ✅ Lesson Planning
echo    ✅ Worksheet Generation
echo    ✅ Reading Assessment
echo    ✅ Visual Aids Generation
echo.
echo 🤖 AI Service: Genkit + Google Gemini
echo 🔑 Requires: Google AI API key in .env file
echo 📍 Get API key: https://ai.google.dev/
echo.

echo Starting FastAPI server...
echo.
echo 📍 Backend URL: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Server startup failed!
    echo 💡 Common fixes:
    echo    - Add GOOGLE_AI_API_KEY to .env file
    echo    - Check if port 8000 is available
    echo    - Verify all dependencies are installed
    echo.
    pause
    exit /b 1
)

pause
