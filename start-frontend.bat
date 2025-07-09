@echo off
echo.
echo ================================
echo   🎨 Starting Sahayak Frontend
echo ================================
echo.
echo 📍 Frontend URL: http://localhost:5173
echo 🌐 Application: Sahayak AI Teaching Assistant
echo.
echo Press Ctrl+C to stop the server
echo ================================
echo.

cd /d "%~dp0sahayak-frontend"
npm run dev

pause 