@echo off
echo Starting llava-phi3 model for worksheet generation...
echo.

echo Pulling llava-phi3 model (this may take a while for first time)...
ollama pull llava-phi3

echo.
echo Testing llava-phi3 model...
echo This is a test prompt | ollama run llava-phi3

echo.
echo llava-phi3 model is ready for worksheet generation!
echo You can now use the worksheet generation feature with vision capabilities.
echo.
pause 