@echo off
echo Creating frontend environment file...

cd sahayak-frontend

(
echo VITE_FIREBASE_API_KEY=AIzaSyDWe4EEjnvBFZgxLTizG4xwsyV3PPFNjB4
echo VITE_FIREBASE_AUTH_DOMAIN=sahayak-ai-platform-6118b.firebaseapp.com
echo VITE_FIREBASE_PROJECT_ID=sahayak-ai-platform-6118b
echo VITE_FIREBASE_STORAGE_BUCKET=sahayak-ai-platform-6118b.firebasestorage.app
echo VITE_FIREBASE_MESSAGING_SENDER_ID=697689176014
echo VITE_FIREBASE_APP_ID=1:697689176014:web:64b7ee45ed20fccabddd9f
echo VITE_FIREBASE_MEASUREMENT_ID=G-VCZBD0FWY7
echo VITE_API_BASE_URL=http://localhost:8000
echo VITE_API_TIMEOUT=30000
echo VITE_APP_NAME=Sahayak
echo VITE_APP_VERSION=1.0.0
echo VITE_ENVIRONMENT=development
echo VITE_ENABLE_ANALYTICS=true
echo VITE_ENABLE_ERROR_REPORTING=true
echo VITE_ENABLE_VOICE_FEATURES=true
echo VITE_ENABLE_OFFLINE_MODE=false
echo VITE_DEFAULT_LANGUAGE=en
echo VITE_SUPPORTED_LANGUAGES=en,hi,mr
echo VITE_THEME=light
echo VITE_DEMO_MODE=false
echo VITE_SHOW_DEMO_DATA=false
) > .env

echo ✅ Frontend environment file created successfully!
echo.
echo The following Firebase configuration has been set:
echo - Firebase Project: sahayak-ai-platform-6118b
echo - API Key: AIzaSyDWe4EEjnvBFZgxLTizG4xwsyV3PPFNjB4
echo - Auth Domain: sahayak-ai-platform-6118b.firebaseapp.com
echo.
echo Your Google sign-in should now work properly!
echo.
pause 