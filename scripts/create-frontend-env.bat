@echo off
echo Creating frontend environment file...

cd sahayak-frontend

(
echo VITE_FIREBASE_API_KEY=your-firebase-api-key-here
echo VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
echo VITE_FIREBASE_PROJECT_ID=your-project-id
echo VITE_FIREBASE_STORAGE_BUCKET=your-project-id.firebasestorage.app
echo VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
echo VITE_FIREBASE_APP_ID=your-app-id
echo VITE_FIREBASE_MEASUREMENT_ID=your-measurement-id
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
echo The following Firebase configuration template has been set:
echo - Firebase Project: your-project-id
echo - API Key: your-firebase-api-key-here  
echo - Auth Domain: your-project-id.firebaseapp.com
echo.
echo Your Google sign-in should now work properly!
echo.
pause 