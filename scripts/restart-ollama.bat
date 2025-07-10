@echo off
title GENKIT AI SERVICE CONFIGURATION CHECK
echo.
echo ============================================
echo  🔧 GENKIT AI SERVICE CONFIGURATION CHECK  
echo ============================================
echo.

echo 📋 Checking Genkit AI Setup...
echo.

echo 🔍 Step 1: Checking Environment Files
echo.

REM Check backend .env file
if exist "sahayak-backend\.env" (
    echo ✅ Backend .env file found
    
    REM Check if Google AI API key exists in .env
    findstr /i "GOOGLE_AI_API_KEY" "sahayak-backend\.env" >nul
    if %errorlevel% equ 0 (
        echo ✅ Google AI API key found in backend .env
    ) else (
        echo ❌ Google AI API key missing from backend .env
        echo 💡 Add: GOOGLE_AI_API_KEY=your_api_key_here
    )
) else (
    echo ❌ Backend .env file not found
    echo 💡 Create sahayak-backend\.env file with your Google AI API key
)

echo.
echo 🔍 Step 2: Checking Google AI API Key Setup
echo.

echo 📋 To get your Google AI API key:
echo    1. Visit: https://ai.google.dev/
echo    2. Click "Get API key"  
echo    3. Sign in with your Google account
echo    4. Click "Create API key"
echo    5. Copy the key to your .env file
echo.

echo 🔍 Step 3: Testing AI Service
echo.

if exist "sahayak-backend\main.py" (
    echo 📋 Testing Genkit AI service...
    cd sahayak-backend
    python -c "from services.genkit_ai_service import GenkitAIService; service = GenkitAIService(); print('✅ Genkit AI service initialized successfully!' if service.genkit_available else '❌ Genkit AI service not available - check API key')"
    cd ..
) else (
    echo ⚠️ Backend files not found
)

echo.
echo ✅ GENKIT CONFIGURATION CHECK COMPLETE
echo.
echo 💡 If you see any errors above:
echo    - Ensure Google AI API key is correctly set in .env
echo    - Restart your backend server after making changes
echo    - Check that internet connection is available
echo.

pause 