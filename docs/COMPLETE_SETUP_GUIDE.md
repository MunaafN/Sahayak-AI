# 🔧 Complete Setup Guide for Sahayak AI Platform

## Overview
This guide provides step-by-step instructions to set up all necessary tools, libraries, and services for the Sahayak AI-powered educational platform.

## 📋 Prerequisites Checklist

### System Requirements
- **Python 3.9+** (for backend)
- **Node.js 18+** (for frontend)
- **npm/yarn** (package manager)
- **Git** (version control)
- **Google Cloud SDK** (for AI services)

### Accounts Needed
- [ ] Google Cloud Platform account
- [ ] Firebase account (uses same Google account)
- [ ] OpenAI account (optional fallback)
- [ ] GitHub account (for deployment)

## 🌐 Google Cloud Platform Setup

### Step 1: Create Google Cloud Project

```bash
# Install Google Cloud SDK first
# Visit: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Create a new project
gcloud projects create sahayak-ai-platform --name="Sahayak AI Platform"

# Set as default project
gcloud config set project sahayak-ai-platform

# Get your project ID
gcloud config get-value project
```

### Step 2: Enable Required APIs

```bash
# Enable all necessary APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable texttospeech.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable firebase.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Verify enabled services
gcloud services list --enabled
```

### Step 3: Create Service Account

```bash
# Create service account for Sahayak
gcloud iam service-accounts create sahayak-ai-service \
    --description="Service account for Sahayak AI platform" \
    --display-name="Sahayak AI Service"

# Get your project ID
PROJECT_ID=$(gcloud config get-value project)

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:sahayak-ai-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:sahayak-ai-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/speech.editor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:sahayak-ai-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:sahayak-ai-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

# Create and download service account key
gcloud iam service-accounts keys create sahayak-credentials.json \
    --iam-account=sahayak-ai-service@$PROJECT_ID.iam.gserviceaccount.com

# Move credentials to secure location
mkdir -p ~/.config/gcloud/
mv sahayak-credentials.json ~/.config/gcloud/sahayak-credentials.json
```

## 🔥 Firebase Setup

### Step 1: Create Firebase Project

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase in your project
cd sahayak-frontend
firebase init

# Select these services:
# - Authentication
# - Firestore Database
# - Storage
# - Hosting (optional)

# Choose existing project (select your Google Cloud project)
```

### Step 2: Configure Firebase Authentication

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Navigate to **Authentication > Sign-in method**
4. Enable:
   - **Email/Password**
   - **Google** (recommended for easy setup)
   - **Anonymous** (for demo users)

### Step 3: Configure Firestore Database

1. In Firebase Console, go to **Firestore Database**
2. Click **Create database**
3. Choose **Start in test mode** for development
4. Select location: **asia-south1** (Mumbai) for India

### Step 4: Configure Firebase Storage

1. Go to **Storage** in Firebase Console
2. Click **Get started**
3. Use default security rules for now
4. Select same location as Firestore

### Step 5: Get Firebase Configuration

1. Go to **Project Settings** (gear icon)
2. Scroll down to **Your apps**
3. Click **Add app** and select **Web**
4. Register app with nickname "Sahayak Frontend"
5. Copy the configuration object

## 📦 Required Libraries and Dependencies

### Backend Dependencies (Python)

```bash
# Navigate to backend directory
cd sahayak-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

**Enhanced `requirements.txt`:**
```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Google Cloud AI
google-cloud-aiplatform==1.38.0
google-cloud-speech==2.21.0
google-cloud-firestore==2.13.1
google-cloud-storage==2.10.0
vertexai==1.38.0

# Firebase
firebase-admin==6.2.0
google-auth==2.23.4

# AI and ML
openai==1.3.5
transformers==4.35.2
torch==2.1.0
nltk==3.8.1
scikit-learn==1.3.2

# Audio Processing
pydub==0.25.1
speechrecognition==3.10.0
librosa==0.10.1

# Image Processing
pillow==10.1.0
opencv-python==4.8.1.78

# Data Processing
pandas==2.1.3
numpy==1.25.2
python-dotenv==1.0.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1

# Authentication & Security
pyjwt[crypto]==2.8.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0

# HTTP Client
httpx==0.25.2
aiohttp==3.9.1

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
```

### Frontend Dependencies (Node.js)

```bash
# Navigate to frontend directory
cd sahayak-frontend

# Install dependencies
npm install
```

**Enhanced `package.json` dependencies:**
```json
{
  "dependencies": {
    "@headlessui/react": "^2.2.4",
    "@heroicons/react": "^2.2.0",
    "@tailwindcss/forms": "^0.5.10",
    "@tailwindcss/typography": "^0.5.16",
    "axios": "^1.10.0",
    "firebase": "^11.10.0",
    "i18next": "^25.3.0",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "react-firebase-hooks": "^5.1.1",
    "react-i18next": "^15.5.3",
    "react-router-dom": "^7.6.3",
    "react-hot-toast": "^2.4.1",
    "react-dropzone": "^14.2.3",
    "wavesurfer.js": "^7.6.0",
    "react-markdown": "^9.0.1",
    "date-fns": "^3.0.6",
    "lucide-react": "^0.525.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.29.0",
    "@types/react": "^19.1.8",
    "@types/react-dom": "^19.1.6",
    "@vitejs/plugin-react": "^4.5.2",
    "autoprefixer": "^10.4.0",
    "eslint": "^9.29.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-react-refresh": "^0.4.20",
    "globals": "^16.2.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "vite": "^5.4.0"
  }
}
```

## 🔐 Environment Variables Configuration

### Backend Environment File (`.env`)

Create `sahayak-backend/.env`:

```bash
# ================================
# SAHAYAK AI PLATFORM CONFIGURATION
# ================================

# ---- APPLICATION SETTINGS ----
APP_NAME=Sahayak AI Platform
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# ---- SECURITY ----
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# ---- GOOGLE CLOUD CONFIGURATION ----
GOOGLE_CLOUD_PROJECT_ID=sahayak-ai-platform
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/sahayak-credentials.json

# Vertex AI Configuration
VERTEX_AI_ENDPOINT=us-central1-aiplatform.googleapis.com
VERTEX_AI_TEXT_MODEL=gemini-pro
VERTEX_AI_VISION_MODEL=gemini-pro-vision
VERTEX_AI_IMAGE_MODEL=imagegeneration@002

# Speech-to-Text Configuration
SPEECH_API_ENDPOINT=speech.googleapis.com
SPEECH_LANGUAGE_CODES=en-US,hi-IN,mr-IN

# ---- FIREBASE CONFIGURATION ----
FIREBASE_PROJECT_ID=sahayak-ai-platform
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=sahayak-ai-service@sahayak-ai-platform.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/sahayak-ai-service%40sahayak-ai-platform.iam.gserviceaccount.com

# ---- DATABASE CONFIGURATION ----
DATABASE_URL=sqlite:///./sahayak.db
# For PostgreSQL (production):
# DATABASE_URL=postgresql://username:password@localhost:5432/sahayak_db

# ---- STORAGE CONFIGURATION ----
GOOGLE_CLOUD_STORAGE_BUCKET=sahayak-ai-platform-storage
UPLOAD_MAX_SIZE=10485760  # 10MB in bytes
ALLOWED_FILE_TYPES=jpg,jpeg,png,gif,pdf,doc,docx,mp3,wav,ogg

# ---- AI SERVICE CONFIGURATION ----
# OpenAI (fallback/alternative)
OPENAI_API_KEY=your-openai-api-key-optional
OPENAI_MODEL=gpt-3.5-turbo

# Content Generation Settings
MAX_CONTENT_LENGTH=2000
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=1000

# ---- CACHING ----
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600  # 1 hour

# ---- EMAIL CONFIGURATION ----
EMAIL_BACKEND=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_USE_TLS=true

# ---- MONITORING & LOGGING ----
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn-for-error-tracking

# ---- RATE LIMITING ----
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# ---- CORS SETTINGS ----
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=*

# ---- DEMO MODE ----
DEMO_MODE=false
MOCK_AI_RESPONSES=false
```

### Frontend Environment File (`.env`)

Create `sahayak-frontend/.env`:

```bash
# ================================
# SAHAYAK FRONTEND CONFIGURATION
# ================================

# ---- FIREBASE CONFIGURATION ----
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=sahayak-ai-platform.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=sahayak-ai-platform
VITE_FIREBASE_STORAGE_BUCKET=sahayak-ai-platform.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:abcdef123456789
VITE_FIREBASE_MEASUREMENT_ID=G-ABCDEFGHIJ

# ---- API CONFIGURATION ----
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# ---- APPLICATION SETTINGS ----
VITE_APP_NAME=Sahayak
VITE_APP_VERSION=1.0.0
VITE_ENVIRONMENT=development

# ---- FEATURE FLAGS ----
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_ERROR_REPORTING=true
VITE_ENABLE_VOICE_FEATURES=true
VITE_ENABLE_OFFLINE_MODE=false

# ---- UI CONFIGURATION ----
VITE_DEFAULT_LANGUAGE=en
VITE_SUPPORTED_LANGUAGES=en,hi,mr
VITE_THEME=light

# ---- DEMO MODE ----
VITE_DEMO_MODE=false
VITE_SHOW_DEMO_DATA=true
```

## 📝 Step-by-Step Setup Process

### Phase 1: Initial Setup (30 minutes)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd sahayak-platform

# 2. Set up backend
cd sahayak-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Set up frontend
cd ../sahayak-frontend
npm install

# 4. Create environment files
cp .env.example .env  # Edit with your values
cd ../sahayak-backend
cp .env.example .env  # Edit with your values
```

### Phase 2: Google Cloud Setup (45 minutes)

```bash
# 1. Install Google Cloud SDK
# Follow: https://cloud.google.com/sdk/docs/install

# 2. Authenticate
gcloud auth login
gcloud auth application-default login

# 3. Create project and enable APIs (run the commands from earlier sections)

# 4. Set up service account (run the commands from earlier sections)

# 5. Test authentication
gcloud auth list
gcloud config list
```

### Phase 3: Firebase Setup (20 minutes)

```bash
# 1. Install Firebase CLI
npm install -g firebase-tools

# 2. Login and initialize
firebase login
cd sahayak-frontend
firebase init

# 3. Configure in Firebase Console (follow earlier steps)

# 4. Update environment variables with Firebase config
```

### Phase 4: Database Setup (15 minutes)

```bash
# 1. Initialize database
cd sahayak-backend
python -c "
from sqlalchemy import create_engine
from models import Base  # assuming you have models
engine = create_engine('sqlite:///sahayak.db')
Base.metadata.create_all(engine)
print('Database initialized successfully!')
"

# 2. Run migrations (if using Alembic)
alembic upgrade head
```

### Phase 5: Testing and Validation (15 minutes)

```bash
# 1. Test backend services
cd sahayak-backend
python setup_ai.py --test

# 2. Start backend
uvicorn main:app --reload --port 8000

# 3. Start frontend (in another terminal)
cd sahayak-frontend
npm run dev

# 4. Open browser and test: http://localhost:5173
```

## 🔍 Verification Commands

### Test Google Cloud Setup
```bash
# Test authentication
gcloud auth list

# Test AI services
python -c "
from google.cloud import aiplatform
aiplatform.init(project='sahayak-ai-platform', location='us-central1')
print('Vertex AI initialized successfully!')
"

# Test Speech-to-Text
python -c "
from google.cloud import speech
client = speech.SpeechClient()
print('Speech client initialized successfully!')
"
```

### Test Firebase Setup
```bash
# Test Firebase Admin SDK
python -c "
import firebase_admin
from firebase_admin import credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
print('Firebase Admin SDK initialized successfully!')
"
```

### Test Frontend Configuration
```bash
# In frontend directory
npm run build
# Should build without errors

# Test Firebase connection
npm run dev
# Check browser console for Firebase connection
```

## 🚨 Common Issues and Solutions

### Issue 1: Google Cloud Authentication
```bash
# If authentication fails:
gcloud auth revoke --all
gcloud auth login
gcloud auth application-default login
```

### Issue 2: Firebase Permissions
```bash
# If Firebase permissions fail:
# 1. Check service account has correct roles
# 2. Verify project ID matches in all configs
# 3. Regenerate service account key if needed
```

### Issue 3: Dependencies Issues
```bash
# Clear and reinstall Python packages
pip freeze > requirements-backup.txt
pip uninstall -r requirements-backup.txt -y
pip install -r requirements.txt

# Clear and reinstall Node packages
rm -rf node_modules package-lock.json
npm install
```

## 🎯 Production Deployment Checklist

### Security
- [ ] Change all default passwords and secret keys
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure proper CORS settings
- [ ] Set up rate limiting
- [ ] Enable authentication and authorization

### Performance
- [ ] Set up Redis for caching
- [ ] Configure CDN for static assets
- [ ] Enable compression
- [ ] Set up database connection pooling
- [ ] Configure load balancing

### Monitoring
- [ ] Set up logging (CloudWatch/Stackdriver)
- [ ] Configure error tracking (Sentry)
- [ ] Set up performance monitoring
- [ ] Configure alerts and notifications
- [ ] Set up backup and recovery

This comprehensive setup will give you a fully functional AI-powered Sahayak platform! 🚀 