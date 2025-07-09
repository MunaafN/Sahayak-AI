@echo off
title Sahayak AI - Complete Startup

echo.
echo ================================================
echo         🚀 SAHAYAK AI TEACHING ASSISTANT
echo ================================================
echo.
echo Starting both Backend and Frontend servers...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo ================================================
echo.

REM Start Backend Server
echo 📦 Starting Backend Server...
start "Sahayak Backend" cmd /k "cd /d \"%~dp0sahayak-backend\" && python main.py"

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start Frontend Server  
echo 🎨 Starting Frontend Server...
start "Sahayak Frontend" cmd /k "cd /d \"%~dp0sahayak-frontend\" && npm run dev"

echo.
echo ✅ Both servers are starting...
echo.
echo 📍 Open your browser and go to: http://localhost:5173
echo.
echo To stop servers: Close both terminal windows
echo.

pause 