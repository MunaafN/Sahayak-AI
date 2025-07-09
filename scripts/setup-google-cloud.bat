@echo off
echo ============================================================
echo    SAHAYAK AI PLATFORM - GOOGLE CLOUD SETUP SCRIPT
echo ============================================================
echo.
echo This script will help you set up Google Cloud Platform
echo for the Sahayak AI Platform.
echo.
echo PREREQUISITES:
echo - Google Cloud SDK installed
echo - Google account with billing enabled
echo - Admin access to create projects
echo.
pause

echo.
echo ============================================================
echo Step 1: Authentication
echo ============================================================
echo Logging in to Google Cloud...
gcloud auth login
if errorlevel 1 (
    echo ERROR: Authentication failed
    pause
    exit /b 1
)

echo.
echo Setting up application default credentials...
gcloud auth application-default login
if errorlevel 1 (
    echo ERROR: Application default credentials setup failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Step 2: Project Setup
echo ============================================================
set /p PROJECT_ID="Enter your project ID (e.g., sahayak-ai-platform): "
if "%PROJECT_ID%"=="" set PROJECT_ID=sahayak-ai-platform

echo Creating project: %PROJECT_ID%
gcloud projects create %PROJECT_ID% --name="Sahayak AI Platform"
if errorlevel 1 (
    echo Project might already exist, continuing...
)

echo Setting project as default...
gcloud config set project %PROJECT_ID%

echo.
echo ============================================================
echo Step 3: Enabling APIs
echo ============================================================
echo This will take a few minutes...

echo Enabling Vertex AI API...
gcloud services enable aiplatform.googleapis.com

echo Enabling Speech-to-Text API...
gcloud services enable speech.googleapis.com

echo Enabling Text-to-Speech API...
gcloud services enable texttospeech.googleapis.com

echo Enabling Cloud Storage API...
gcloud services enable storage.googleapis.com

echo Enabling Firestore API...
gcloud services enable firestore.googleapis.com

echo Enabling Firebase APIs...
gcloud services enable firebase.googleapis.com
gcloud services enable firebaserules.googleapis.com

echo Enabling other required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com

echo.
echo ============================================================
echo Step 4: Service Account Creation
echo ============================================================
echo Creating service account...
gcloud iam service-accounts create sahayak-ai-service --description="Service account for Sahayak AI platform" --display-name="Sahayak AI Service"

echo.
echo Granting roles to service account...
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:sahayak-ai-service@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/aiplatform.user"
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:sahayak-ai-service@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/speech.editor"
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:sahayak-ai-service@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:sahayak-ai-service@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/datastore.user"
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:sahayak-ai-service@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/firebase.admin"

echo.
echo Creating and downloading service account key...
gcloud iam service-accounts keys create sahayak-credentials.json --iam-account=sahayak-ai-service@%PROJECT_ID%.iam.gserviceaccount.com

echo.
echo Moving credentials to backend directory...
move sahayak-credentials.json sahayak-backend\sahayak-credentials.json

echo.
echo ============================================================
echo Step 5: Environment Variables Setup
echo ============================================================
echo.
echo Creating backend environment file...
(
echo # ================================
echo # SAHAYAK AI PLATFORM CONFIGURATION
echo # ================================
echo.
echo # ---- APPLICATION SETTINGS ----
echo APP_NAME=Sahayak AI Platform
echo APP_VERSION=1.0.0
echo DEBUG=true
echo ENVIRONMENT=development
echo.
echo # ---- SECURITY ----
echo SECRET_KEY=your-super-secret-key-change-this-in-production
echo JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
echo JWT_ALGORITHM=HS256
echo JWT_EXPIRATION_HOURS=24
echo.
echo # ---- GOOGLE CLOUD CONFIGURATION ----
echo GOOGLE_CLOUD_PROJECT_ID=%PROJECT_ID%
echo GOOGLE_CLOUD_LOCATION=us-central1
echo GOOGLE_APPLICATION_CREDENTIALS=./sahayak-credentials.json
echo.
echo # ---- VERTEX AI CONFIGURATION ----
echo VERTEX_AI_ENDPOINT=us-central1-aiplatform.googleapis.com
echo VERTEX_AI_TEXT_MODEL=gemini-pro
echo VERTEX_AI_VISION_MODEL=gemini-pro-vision
echo VERTEX_AI_IMAGE_MODEL=imagegeneration@002
echo.
echo # ---- SPEECH-TO-TEXT CONFIGURATION ----
echo SPEECH_API_ENDPOINT=speech.googleapis.com
echo SPEECH_LANGUAGE_CODES=en-US,hi-IN,mr-IN
echo.
echo # ---- FIREBASE CONFIGURATION ----
echo FIREBASE_PROJECT_ID=%PROJECT_ID%
echo FIREBASE_PRIVATE_KEY_ID=your-private-key-id-from-json
echo FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_FROM_JSON\n-----END PRIVATE KEY-----\n"
echo FIREBASE_CLIENT_EMAIL=sahayak-ai-service@%PROJECT_ID%.iam.gserviceaccount.com
echo FIREBASE_CLIENT_ID=your-client-id-from-json
echo FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/sahayak-ai-service%%40%PROJECT_ID%.iam.gserviceaccount.com
echo.
echo # ---- STORAGE CONFIGURATION ----
echo GOOGLE_CLOUD_STORAGE_BUCKET=%PROJECT_ID%.appspot.com
echo UPLOAD_MAX_SIZE=10485760
echo ALLOWED_FILE_TYPES=jpg,jpeg,png,gif,pdf,doc,docx,mp3,wav,ogg
echo.
echo # ---- AI SERVICE CONFIGURATION ----
echo OPENAI_API_KEY=your-openai-api-key-optional
echo OPENAI_MODEL=gpt-3.5-turbo
echo MAX_CONTENT_LENGTH=2000
echo DEFAULT_TEMPERATURE=0.7
echo DEFAULT_MAX_TOKENS=1000
echo.
echo # ---- DATABASE CONFIGURATION ----
echo DATABASE_URL=sqlite:///./sahayak.db
echo.
echo # ---- NETWORKING ^& SECURITY ----
echo ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
echo ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
echo ALLOWED_HEADERS=*
echo RATE_LIMIT_PER_MINUTE=60
echo RATE_LIMIT_PER_HOUR=1000
echo.
echo # ---- DEMO MODE ----
echo DEMO_MODE=false
echo MOCK_AI_RESPONSES=false
) > sahayak-backend\.env

echo.
echo ============================================================
echo SETUP COMPLETE!
echo ============================================================
echo.
echo ✅ Google Cloud Project: %PROJECT_ID%
echo ✅ APIs enabled
echo ✅ Service account created
echo ✅ Credentials downloaded
echo ✅ Environment file created
echo.
echo NEXT STEPS:
echo.
echo 1. Set up Firebase Console:
echo    - Go to https://console.firebase.google.com/
echo    - Add project and select '%PROJECT_ID%'
echo    - Enable Authentication, Firestore, and Storage
echo    - Get web app config and update frontend .env
echo.
echo 2. Update Firebase credentials in backend .env:
echo    - Open sahayak-backend\sahayak-credentials.json
echo    - Copy private_key_id, private_key, client_id to .env
echo.
echo 3. Generate security keys:
echo    - Run: python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
echo    - Replace SECRET_KEY and JWT_SECRET_KEY in .env
echo.
echo 4. Test the setup:
echo    - Run: cd sahayak-backend
echo    - Run: python setup_ai.py --test
echo.
echo 📚 For detailed instructions, see: docs\GOOGLE_SETUP_GUIDE.md
echo.
pause 