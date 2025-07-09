@echo off
echo ========================================
echo SAHAYAK PLATFORM - STARTUP
echo ========================================

echo 🔍 Pre-flight Checks...

REM Check backend credentials
if not exist "sahayak-backend\sahayak-credentials.json" (
    echo ❌ Backend Google Cloud credentials missing!
    echo 📄 Expected: sahayak-backend\sahayak-credentials.json
    pause
    exit /b 1
)
echo ✅ Backend Google Cloud credentials found

REM Check/Create backend .env
if not exist "sahayak-backend\.env" (
    echo 📋 Creating backend environment configuration...
    copy "config\backend-env-actual.txt" "sahayak-backend\.env"
)
echo ✅ Backend environment configured

REM Check/Create frontend .env  
if not exist "sahayak-frontend\.env" (
    echo 📋 Creating frontend environment configuration...
    call scripts\create-frontend-env.bat
)
echo ✅ Frontend environment configured

echo.
echo 🤖 Initializing AI Models...
echo 📥 Starting llava-phi3 for vision-based worksheets...
start /min cmd /c "ollama run llava-phi3 & exit"

echo ⏳ Waiting for AI model initialization...
timeout /t 3 /nobreak >nul

echo.
echo 🚀 Starting Sahayak Platform Services...
echo ================================

echo 🔧 Starting Backend Server...
start "Sahayak Backend" cmd /c scripts\start-backend.bat

echo ⏳ Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

echo 🎨 Starting Frontend Server...
start "Sahayak Frontend" cmd /c scripts\start-frontend.bat

echo.
echo ✅ Both servers are starting...
echo 📍 Backend: http://localhost:8000
echo 📍 Frontend: http://localhost:5173
echo 📚 API Docs: http://localhost:8000/docs
echo 🔐 Google Auth: READY
echo 🤖 AI Models: READY
echo ========================================
echo 💡 Both servers will open in separate windows
echo 💡 Close this window to keep servers running
echo ========================================
pause
