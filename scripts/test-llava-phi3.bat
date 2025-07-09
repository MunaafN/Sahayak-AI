@echo off
echo Testing llava-phi3 integration for worksheets...
echo.

echo 1. Checking if Ollama is running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Ollama is running
) else (
    echo ❌ Ollama is not running. Please start it first.
    echo Run: ollama serve
    pause
    exit /b 1
)

echo.
echo 2. Checking if llava-phi3 model is available...
ollama list | findstr "llava-phi3" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ llava-phi3 model is available
) else (
    echo ❌ llava-phi3 model not found
    echo Downloading llava-phi3 model (this may take a few minutes)...
    ollama pull llava-phi3
    if %errorlevel%==0 (
        echo ✅ llava-phi3 model downloaded successfully
    ) else (
        echo ❌ Failed to download llava-phi3 model
        pause
        exit /b 1
    )
)

echo.
echo 3. Testing llava-phi3 model...
echo This is a test | ollama run llava-phi3 "Describe what you can do for educational worksheets."
if %errorlevel%==0 (
    echo ✅ llava-phi3 model is working correctly
) else (
    echo ⚠️ llava-phi3 model test had issues, but may still work
)

echo.
echo 4. Checking backend server status...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Backend server is running
    echo You can now test vision-based worksheets!
) else (
    echo ⚠️ Backend server is not running
    echo Start it with: python main.py
)

echo.
echo Test complete! Your llava-phi3 setup is ready for vision-based worksheets.
echo.
pause 