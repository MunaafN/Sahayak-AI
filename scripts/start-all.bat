@echo off
title SAHAYAK FULL PLATFORM STARTUP
echo.
echo ============================================
echo  🚀 SAHAYAK FULL PLATFORM STARTUP  
echo ============================================
echo.

echo 📋 Starting Complete Sahayak Platform...
echo.

echo 🔧 Platform Components:
echo    🎯 Frontend: React + Vite (Port 5173)
echo    🔧 Backend: FastAPI (Port 8000)  
echo    🤖 AI Service: Genkit + Google Gemini
echo    🔐 Authentication: Firebase Auth
echo.

echo 📋 Step 1: Starting Backend Server
echo.
start "Backend Server" cmd /k "cd sahayak-backend && python main.py"

echo ⏳ Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo.
echo 📋 Step 2: Starting Frontend Application
echo.
start "Frontend App" cmd /k "cd sahayak-frontend && npm run dev"

echo.
echo ✅ SAHAYAK PLATFORM STARTUP COMPLETE!
echo.
echo 📍 Access Points:
echo    🌐 Frontend: http://localhost:5173
echo    🔧 Backend API: http://localhost:8000  
echo    📚 API Docs: http://localhost:8000/docs
echo.
echo 🔑 Important: Ensure you have GOOGLE_AI_API_KEY in your .env files
echo 📖 Get API key from: https://ai.google.dev/
echo.

pause
