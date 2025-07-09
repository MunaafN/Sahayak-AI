@echo off
echo ================================================
echo 🔄 RESTARTING OLLAMA SERVICE (Memory Fix)
echo ================================================

echo.
echo 🛑 Stopping Ollama service...
taskkill /f /im ollama.exe 2>nul
timeout /t 2 /nobreak >nul

echo ✅ Ollama stopped
echo.
echo 🧠 Clearing memory...
timeout /t 3 /nobreak >nul

echo.
echo 🚀 Starting Ollama service...
start /min ollama serve

echo ⏳ Waiting for service to start...
timeout /t 5 /nobreak >nul

echo.
echo 🔍 Testing service availability...
curl -s http://localhost:11434/api/tags >nul
if %errorlevel% equ 0 (
    echo ✅ Ollama service is running
) else (
    echo ❌ Ollama service failed to start
    echo 💡 Please install Ollama from https://ollama.ai/
    pause
    exit /b 1
)

echo.
echo 📥 Ensuring models are available...
ollama pull llama3:8b
ollama pull llava-phi3:latest

echo.
echo ================================================
echo ✅ OLLAMA RESTART COMPLETE
echo ================================================
echo 🧠 Memory-efficient models ready:
echo    - llama3:8b (text generation)
echo    - llava-phi3:latest (vision)
echo.
echo 💡 You can now start the backend with: python main.py
echo ================================================

pause 