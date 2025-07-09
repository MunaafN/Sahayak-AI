@echo off
echo ================================
echo SAHAYAK FRONTEND - GOOGLE AUTH READY
echo ================================

cd sahayak-frontend

echo 🔍 Checking Firebase Authentication Setup...
if not exist ".env" (
    echo 📋 Creating frontend environment configuration...
    copy "..\config\frontend-env-actual.txt" ".env"
    if exist ".env" (
        echo ✅ Frontend .env file created with Firebase config
    ) else (
        echo ❌ Could not create .env file
        echo 💡 Please manually copy config\frontend-env-actual.txt to sahayak-frontend\.env
        pause
        exit /b 1
    )
) else (
    echo ✅ Frontend .env file exists
)

echo 🔍 Checking Node.js Dependencies...
if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    npm install
) else (
    echo ✅ Node.js dependencies found
)

echo 🚀 Starting Sahayak Frontend...
echo 📍 URL: http://localhost:5173
echo 🔐 Firebase Auth: READY
echo 🎨 React + Vite: READY
echo ================================

npm run dev
pause
