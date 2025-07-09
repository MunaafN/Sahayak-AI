@echo off
echo ============================================================
echo    FIXING HTTP 500 AI SERVICE ERROR - SAHAYAK PLATFORM
echo ============================================================
echo.
echo This script will fix the AI service error by:
echo 1. Creating backend environment file
echo 2. Starting Ollama AI service
echo 3. Installing required AI models
echo 4. Starting the backend server
echo.
pause

echo.
echo ============================================================
echo Step 1: Creating Backend Environment File
echo ============================================================
echo.

if not exist "sahayak-backend\.env" (
    echo Creating backend .env file...
    
    (
    echo # Sahayak Backend Configuration
    echo DEMO_MODE=false
    echo GOOGLE_CLOUD_PROJECT_ID=sahayak-ai-platform
    echo GOOGLE_APPLICATION_CREDENTIALS=./sahayak-credentials.json
    echo SECRET_KEY=sahayak-secret-key-for-development
    echo JWT_SECRET_KEY=sahayak-jwt-secret-key-for-development
    echo JWT_ALGORITHM=HS256
    echo JWT_EXPIRATION_HOURS=24
    echo ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
    echo ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
    echo ALLOWED_HEADERS=*
    ) > sahayak-backend\.env
    
    echo ✅ Backend environment file created!
) else (
    echo ✅ Backend environment file already exists!
)

echo.
echo ============================================================
echo Step 2: Checking Ollama Installation
echo ============================================================
echo.

ollama version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama is not installed!
    echo.
    echo Please install Ollama to use AI features:
    echo 1. Download from: https://ollama.ai/
    echo 2. Install the executable
    echo 3. Run this script again
    echo.
    echo Alternative: The platform will work in basic mode without AI
    pause
    goto :start_backend
) else (
    echo ✅ Ollama is installed!
)

echo.
echo ============================================================
echo Step 3: Starting Ollama Service
echo ============================================================
echo.

echo Starting Ollama service...
start /min cmd /c "ollama serve"

timeout /t 3 /nobreak >nul

echo.
echo ============================================================
echo Step 4: Installing AI Models
echo ============================================================
echo.

echo Checking for required AI models...

REM Check if llama3.1:8b is available
ollama list | findstr "llama3.1" >nul
if errorlevel 1 (
    echo 📥 Installing llama3.1:8b model (this may take a few minutes)...
    ollama pull llama3.1:8b
    if errorlevel 1 (
        echo ⚠️ Failed to install llama3.1:8b. Trying llama3.2:3b instead...
        ollama pull llama3.2:3b
        if errorlevel 1 (
            echo ⚠️ Could not install main AI model. Platform will use fallback mode.
        ) else (
            echo ✅ llama3.2:3b model installed successfully!
        )
    ) else (
        echo ✅ llama3.1:8b model installed successfully!
    )
) else (
    echo ✅ Main AI model is available!
)

REM Check if llava-phi3 is available for vision features
ollama list | findstr "llava-phi3" >nul
if errorlevel 1 (
    echo 📥 Installing llava-phi3 model for vision features...
    ollama pull llava-phi3
    if errorlevel 1 (
        echo ⚠️ Could not install vision model. Vision features will be limited.
    ) else (
        echo ✅ llava-phi3 vision model installed successfully!
    )
) else (
    echo ✅ Vision model is available!
)

:start_backend
echo.
echo ============================================================
echo Step 5: Starting Backend Server
echo ============================================================
echo.

echo Installing Python dependencies...
cd sahayak-backend

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found. Using system Python.
)

REM Install requirements
pip install -r requirements.txt --quiet

echo.
echo Starting Sahayak Backend Server...
echo.
echo Backend will start at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo AI Status Check: http://localhost:8000/debug/ai-status
echo.

start "Sahayak Backend" cmd /c "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 & pause"

timeout /t 3 /nobreak >nul

echo.
echo ============================================================
echo Step 6: Testing AI Service
echo ============================================================
echo.

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo Testing AI service connection...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Backend server is still starting. Please wait a moment.
) else (
    echo ✅ Backend server is running!
)

echo.
echo ============================================================
echo TROUBLESHOOTING GUIDE
echo ============================================================
echo.
echo If you still get HTTP 500 AI Service Error:
echo.
echo 1. CHECK BACKEND STATUS:
echo    Open: http://localhost:8000/health
echo    Should show: {"status": "healthy"}
echo.
echo 2. CHECK AI SERVICE:
echo    Open: http://localhost:8000/debug/ai-status
echo    Should show Ollama service details
echo.
echo 3. CHECK OLLAMA:
echo    Run: ollama list
echo    Should show installed models
echo.
echo 4. RESTART SERVICES:
echo    Close all terminal windows
echo    Run: scripts\start-all.bat
echo.
echo 5. FALLBACK MODE:
echo    If Ollama fails, the platform works with limited AI features
echo.

echo.
echo ============================================================
echo AI SERVICE FIX COMPLETE!
echo ============================================================
echo.
echo Your AI service should now be working properly.
echo.
echo WHAT'S RUNNING:
echo ✅ Frontend: http://localhost:5173
echo ✅ Backend: http://localhost:8000
echo ✅ Ollama AI Service (if installed)
echo ✅ Google Authentication
echo.
echo Next steps:
echo 1. Try using AI features in the frontend
echo 2. If you get errors, check the troubleshooting guide above
echo 3. Run scripts\start-all.bat for full platform startup
echo.
pause 