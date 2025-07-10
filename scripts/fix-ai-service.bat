@echo off
title GENKIT AI SERVICE SETUP HELPER
echo.
echo ============================================
echo  🔧 GENKIT AI SERVICE SETUP HELPER
echo ============================================
echo.

echo 📋 This script will help you set up Genkit AI service
echo.

echo 🔧 GENKIT AI SETUP PROCESS:
echo    1. Install required Python packages
echo    2. Configure Google AI API key
echo    3. Test the AI service
echo    4. Provide usage instructions
echo.

echo 📋 Step 1: Installing Required Packages
echo.

cd sahayak-backend

echo 🐍 Installing Genkit and dependencies...
pip install google-generativeai==0.3.2
if %errorlevel% neq 0 (
    echo ❌ Failed to install google-generativeai
    pause
    exit /b 1
)

pip install "genkit[google-ai]==0.5.2"
if %errorlevel% neq 0 (
    echo ❌ Failed to install genkit
    pause
    exit /b 1
)

pip install pydantic-ai==0.0.8
if %errorlevel% neq 0 (
    echo ❌ Failed to install pydantic-ai
    pause
    exit /b 1
)

echo ✅ All packages installed successfully!

echo.
echo 📋 Step 2: Google AI API Key Setup
echo.

if not exist ".env" (
    echo 📋 Creating .env file...
    echo # Sahayak Backend Configuration > .env
    echo GOOGLE_AI_API_KEY=your_google_ai_api_key_here >> .env
    echo. >> .env
    echo ✅ .env file created
) else (
    findstr /i "GOOGLE_AI_API_KEY" ".env" >nul
    if %errorlevel% neq 0 (
        echo 📋 Adding Google AI API key to existing .env...
        echo GOOGLE_AI_API_KEY=your_google_ai_api_key_here >> .env
    )
)

echo.
echo 🔑 IMPORTANT: You need to get your Google AI API key:
echo.
echo 📋 How to get Google AI API key:
echo    1. Visit: https://ai.google.dev/
echo    2. Click "Get API key in Google AI Studio"
echo    3. Sign in with your Google account
echo    4. Click "Create API key"
echo    5. Copy the key (starts with 'AIza...')
echo.
echo 📝 Edit the .env file and replace 'your_google_ai_api_key_here' with your actual key
echo.

pause
echo.

echo 📋 Step 3: Testing AI Service
echo.

echo 🧪 Testing Genkit AI service...
python -c "from services.genkit_ai_service import GenkitAIService; service = GenkitAIService(); print('✅ Genkit AI service working!' if service.genkit_available else '❌ API key needed - edit .env file')"

echo.
echo 📋 Step 4: Usage Instructions
echo.

echo ✅ GENKIT AI SETUP COMPLETE!
echo.
echo 🚀 To start using Sahayak with Genkit AI:
echo    1. Ensure your Google AI API key is in .env file
echo    2. Run: python main.py (or use start-backend.bat)
echo    3. Open: http://localhost:8000
echo.
echo 🎯 Benefits of Genkit AI:
echo    ✅ Better Hindi grammar and accuracy
echo    ✅ Superior factual content
echo    ✅ Faster response times
echo    ✅ Better educational content quality
echo    ✅ Built-in prompt optimization
echo.
echo 💰 Cost: FREE tier with generous limits
echo 📊 Monthly usage: Typically $0-15 for educational use
echo.

cd ..
pause 