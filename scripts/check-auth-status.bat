@echo off
echo ================================
echo SAHAYAK AUTHENTICATION STATUS CHECK
echo ================================

echo 🔍 Backend Authentication Status:
echo.

REM Check backend credentials
if exist "sahayak-backend\sahayak-credentials.json" (
    echo ✅ Google Cloud credentials: FOUND
) else (
    echo ❌ Google Cloud credentials: MISSING
)

REM Check backend .env
if exist "sahayak-backend\.env" (
    echo ✅ Backend .env file: FOUND
) else (
    echo ❌ Backend .env file: MISSING
)

echo.
echo 🔍 Frontend Authentication Status:
echo.

REM Check frontend .env
if exist "sahayak-frontend\.env" (
    echo ✅ Frontend .env file: FOUND
    
    REM Check if it contains Firebase config
    findstr /c:"VITE_FIREBASE_API_KEY=" "sahayak-frontend\.env" >nul
    if !errorlevel! equ 0 (
        echo ✅ Firebase API Key: CONFIGURED
    ) else (
        echo ⚠️ Firebase API Key: CHECK CONFIGURATION
    )
    
    findstr /c:"VITE_FIREBASE_PROJECT_ID=" "sahayak-frontend\.env" >nul
    if !errorlevel! equ 0 (
        echo ✅ Firebase Project ID: CONFIGURED
    ) else (
        echo ⚠️ Firebase Project ID: CHECK CONFIGURATION
    )
    
) else (
    echo ❌ Frontend .env file: MISSING
)

echo.
echo 🔍 AI Models Status:
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Ollama Service: RUNNING
) else (
    echo ❌ Ollama Service: NOT RUNNING
)

echo.
echo 🔍 Server Status:
echo.

REM Check backend server
curl -s http://localhost:8000/health >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Backend Server: RUNNING (http://localhost:8000)
) else (
    echo ❌ Backend Server: NOT RUNNING
)

REM Check frontend server
curl -s http://localhost:5173 >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Frontend Server: RUNNING (http://localhost:5173)
) else (
    echo ❌ Frontend Server: NOT RUNNING
)

echo.
echo ================================
echo 💡 If any items show ❌ or ⚠️, run:
echo 💡 scripts\start-all.bat
echo ================================
pause 