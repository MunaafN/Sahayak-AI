@echo off
echo ================================================
echo 🧪 TESTING SAHAYAK BACKEND AI SERVICE
echo ================================================

cd /d "%~dp0..\sahayak-backend"

echo.
echo 🔍 Testing Ollama service availability...
curl -s http://localhost:11434/api/tags > nul
if %errorlevel% equ 0 (
    echo ✅ Ollama is running on localhost:11434
) else (
    echo ❌ Ollama is not running - will be started by backend
)

echo.
echo 🔍 Checking for required models...
ollama list | find "llama3" > nul
if %errorlevel% equ 0 (
    echo ✅ llama3 model is available
) else (
    echo ⚠️ llama3 model not found - will be downloaded
)

ollama list | find "llava-phi3" > nul
if %errorlevel% equ 0 (
    echo ✅ llava-phi3 model is available
) else (
    echo ⚠️ llava-phi3 model not found - will be downloaded
)

echo.
echo 🚀 Starting Sahayak Backend with AI models...
echo 📍 Backend will be available at: http://localhost:8000
echo 📚 API docs will be at: http://localhost:8000/docs
echo 🤖 AI status check: http://localhost:8000/debug/ai-status
echo.
echo ⏹️ Press Ctrl+C to stop the server
echo ================================================

python main.py

pause 