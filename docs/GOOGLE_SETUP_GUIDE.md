# 🔑 Google Technologies Setup for Sahayak AI Platform

This guide provides **exact steps** to set up all Google technologies needed for AI features.

## 📋 Required Google Technologies

1. **Google Cloud Platform (GCP)** - Main platform
2. **Firebase** - Authentication & Database  
3. **Vertex AI** - AI models (Gemini Pro)
4. **Google Cloud Speech-to-Text** - Voice recognition
5. **Google Cloud Storage** - File storage
6. **Google Cloud Firestore** - Database

---

## 🚀 Step-by-Step Setup Process

### **Step 1: Create Google Cloud Platform Account**

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Sign in** with your Google account (or create one)
3. **Accept Terms of Service** if prompted
4. **Set up billing** (required for AI services):
   - Click "Billing" in the left sidebar
   - Add a payment method
   - ⚠️ **Note**: Google gives $300 free credits for new users

### **Step 2: Create a New Project**

1. **Click the project dropdown** at the top
2. **Click "New Project"**
3. **Enter project details**:
   - Project name: `Sahayak AI Platform`
   - Project ID: `sahayak-ai-platform` (must be unique globally)
   - Location: Select your organization or leave as "No organization"
4. **Click "Create"**
5. **Wait for project creation** (takes ~30 seconds)
6. **Select your new project** from the dropdown

### **Step 3: Enable Required APIs**

1. **Go to "APIs & Services" > "Library"**
2. **Search and enable these APIs** (click each, then click "Enable"):

   **AI & ML APIs:**
   - `Vertex AI API`
   - `Cloud Speech-to-Text API`
   - `Cloud Text-to-Speech API`
   
   **Storage & Database APIs:**
   - `Cloud Storage API`
   - `Cloud Firestore API`
   
   **Firebase APIs:**
   - `Firebase Management API`
   - `Firebase Rules API`
   
   **General APIs:**
   - `Cloud Build API`
   - `Cloud Run API`
   - `Secret Manager API`

3. **Wait for each API to be enabled** (takes 1-2 minutes each)

### **Step 4: Create Service Account & Download Credentials**

1. **Go to "IAM & Admin" > "Service Accounts"**
2. **Click "Create Service Account"**
3. **Enter service account details**:
   - Service account name: `sahayak-ai-service`
   - Service account ID: `sahayak-ai-service` (auto-filled)
   - Description: `Service account for Sahayak AI platform`
4. **Click "Create and Continue"**

5. **Grant roles** (click "Add Role" for each):
   - `Vertex AI User`
   - `Speech Editor`
   - `Cloud Storage Admin`
   - `Cloud Datastore User`
   - `Firebase Admin`
   - `Service Account Token Creator`

6. **Click "Continue" then "Done"**

7. **Download the credentials**:
   - Click on your new service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Select "JSON" format
   - Click "Create"
   - **Save the downloaded file** as `sahayak-credentials.json`

### **Step 5: Set Up Firebase**

1. **Go to Firebase Console**: https://console.firebase.google.com/
2. **Click "Add Project"**
3. **Select your existing Google Cloud project**: `sahayak-ai-platform`
4. **Configure Firebase**:
   - Enable Google Analytics: **Yes** (recommended)
   - Analytics account: Select existing or create new
5. **Click "Create Project"**

### **Step 6: Configure Firebase Services**

#### **6.1 Set Up Authentication**
1. **Go to "Authentication"** in Firebase Console
2. **Click "Get Started"**
3. **Go to "Sign-in method" tab**
4. **Enable these providers**:
   - **Email/Password**: Click → Toggle "Enable" → Save
   - **Google**: Click → Toggle "Enable" → Select support email → Save
   - **Anonymous**: Click → Toggle "Enable" → Save

#### **6.2 Set Up Firestore Database**
1. **Go to "Firestore Database"**
2. **Click "Create database"**
3. **Choose "Start in test mode"** (for development)
4. **Select location**: `asia-south1 (Mumbai)` (closest to India)
5. **Click "Done"**

#### **6.3 Set Up Storage**
1. **Go to "Storage"**
2. **Click "Get started"**
3. **Choose "Start in test mode"**
4. **Select same location**: `asia-south1 (Mumbai)`
5. **Click "Done"**

### **Step 7: Get Firebase Configuration**

1. **Go to Project Settings** (⚙️ icon in Firebase Console)
2. **Scroll to "Your apps" section**
3. **Click the Web app icon** `</>`
4. **Register app**:
   - App nickname: `Sahayak Frontend`
   - Check "Also set up Firebase Hosting" (optional)
   - Click "Register app"
5. **Copy the configuration object** (looks like this):

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC...",
  authDomain: "sahayak-ai-platform.firebaseapp.com",
  projectId: "sahayak-ai-platform",
  storageBucket: "sahayak-ai-platform.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456789"
};
```

### **Step 8: Get Service Account Private Key Details**

1. **Open the downloaded `sahayak-credentials.json` file**
2. **Copy these values** (you'll need them for env file):
   - `private_key_id`
   - `private_key`
   - `client_email`
   - `client_id`
   - `client_x509_cert_url`

---

## 📝 Environment Variables Setup

### **Backend Environment File (`sahayak-backend/.env`)**

Create a file called `.env` in the `sahayak-backend` directory with this content:

```bash
# ================================
# SAHAYAK AI PLATFORM CONFIGURATION
# ================================

# ---- APPLICATION SETTINGS ----
APP_NAME=Sahayak AI Platform
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# ---- SECURITY (GENERATE RANDOM KEYS) ----
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# ================================
# GOOGLE CLOUD CONFIGURATION
# ================================
# Replace with your actual Google Cloud project ID
GOOGLE_CLOUD_PROJECT_ID=sahayak-ai-platform
GOOGLE_CLOUD_LOCATION=us-central1
# Path to your downloaded credentials JSON file
GOOGLE_APPLICATION_CREDENTIALS=./sahayak-credentials.json

# ---- VERTEX AI CONFIGURATION ----
VERTEX_AI_ENDPOINT=us-central1-aiplatform.googleapis.com
VERTEX_AI_TEXT_MODEL=gemini-pro
VERTEX_AI_VISION_MODEL=gemini-pro-vision
VERTEX_AI_IMAGE_MODEL=imagegeneration@002

# ---- SPEECH-TO-TEXT CONFIGURATION ----
SPEECH_API_ENDPOINT=speech.googleapis.com
SPEECH_LANGUAGE_CODES=en-US,hi-IN,mr-IN

# ================================
# FIREBASE CONFIGURATION
# ================================
# Replace with values from your sahayak-credentials.json file
FIREBASE_PROJECT_ID=sahayak-ai-platform
FIREBASE_PRIVATE_KEY_ID=your-private-key-id-from-json
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_FROM_JSON\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=sahayak-ai-service@sahayak-ai-platform.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id-from-json
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/sahayak-ai-service%40sahayak-ai-platform.iam.gserviceaccount.com

# ================================
# STORAGE CONFIGURATION
# ================================
GOOGLE_CLOUD_STORAGE_BUCKET=sahayak-ai-platform.appspot.com
UPLOAD_MAX_SIZE=10485760
ALLOWED_FILE_TYPES=jpg,jpeg,png,gif,pdf,doc,docx,mp3,wav,ogg

# ================================
# AI SERVICE CONFIGURATION
# ================================
# OpenAI (optional fallback)
OPENAI_API_KEY=your-openai-api-key-optional
OPENAI_MODEL=gpt-3.5-turbo

# Content Generation Settings
MAX_CONTENT_LENGTH=2000
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=1000

# ================================
# DATABASE CONFIGURATION
# ================================
DATABASE_URL=sqlite:///./sahayak.db

# ================================
# NETWORKING & SECURITY
# ================================
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=*
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# ================================
# DEMO MODE (SET TO FALSE FOR REAL AI)
# ================================
DEMO_MODE=false
MOCK_AI_RESPONSES=false
```

### **Frontend Environment File (`sahayak-frontend/.env`)**

Create a file called `.env` in the `sahayak-frontend` directory with this content:

```bash
# ================================
# SAHAYAK FRONTEND CONFIGURATION
# ================================

# ---- FIREBASE CONFIGURATION ----
# Replace with values from Firebase Console > Project Settings > General > Your apps
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

# ================================
# DEMO MODE (SET TO FALSE FOR REAL AI)
# ================================
VITE_DEMO_MODE=false
VITE_SHOW_DEMO_DATA=false
```

---

## 🔧 Exact Steps to Fill Environment Variables

### **Step 1: Replace Google Cloud Project ID**

In both `.env` files, replace:
```bash
GOOGLE_CLOUD_PROJECT_ID=sahayak-ai-platform
```
With your actual project ID (if different).

### **Step 2: Place Credentials File**

1. **Copy the downloaded `sahayak-credentials.json`** to the `sahayak-backend` directory
2. **Update the path** in backend `.env`:
```bash
GOOGLE_APPLICATION_CREDENTIALS=./sahayak-credentials.json
```

### **Step 3: Fill Firebase Service Account Details**

1. **Open `sahayak-credentials.json`** in a text editor
2. **Copy these values** to backend `.env`:

```bash
# From sahayak-credentials.json, copy these exact values:
FIREBASE_PRIVATE_KEY_ID=copy-private_key_id-here
FIREBASE_PRIVATE_KEY="copy-private_key-here-with-quotes"
FIREBASE_CLIENT_EMAIL=copy-client_email-here
FIREBASE_CLIENT_ID=copy-client_id-here
FIREBASE_CLIENT_X509_CERT_URL=copy-client_x509_cert_url-here
```

### **Step 4: Fill Firebase Web App Config**

1. **From Firebase Console > Project Settings > General > Your apps**
2. **Copy the config values** to frontend `.env`:

```bash
# From Firebase web app config, copy these values:
VITE_FIREBASE_API_KEY=copy-apiKey-here
VITE_FIREBASE_AUTH_DOMAIN=copy-authDomain-here
VITE_FIREBASE_PROJECT_ID=copy-projectId-here
VITE_FIREBASE_STORAGE_BUCKET=copy-storageBucket-here
VITE_FIREBASE_MESSAGING_SENDER_ID=copy-messagingSenderId-here
VITE_FIREBASE_APP_ID=copy-appId-here
VITE_FIREBASE_MEASUREMENT_ID=copy-measurementId-here
```

### **Step 5: Generate Security Keys**

Generate random keys for security:

```bash
# Run this in terminal to generate keys:
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

Replace the generated keys in backend `.env`.

---

## 🧪 Testing Your Setup

### **Test 1: Check Google Cloud Authentication**

```bash
cd sahayak-backend
python -c "
import os
from google.cloud import aiplatform
from dotenv import load_dotenv

load_dotenv()
project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
location = os.getenv('GOOGLE_CLOUD_LOCATION')

aiplatform.init(project=project_id, location=location)
print('✅ Google Cloud AI Platform initialized successfully!')
"
```

### **Test 2: Check Firebase Connection**

```bash
cd sahayak-backend
python -c "
import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()
cred = credentials.Certificate('./sahayak-credentials.json')
firebase_admin.initialize_app(cred)
print('✅ Firebase Admin SDK initialized successfully!')
"
```

### **Test 3: Check Speech-to-Text**

```bash
cd sahayak-backend
python -c "
from google.cloud import speech
client = speech.SpeechClient()
print('✅ Speech-to-Text client initialized successfully!')
"
```

### **Test 4: Start the Application**

```bash
# Start backend
cd sahayak-backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --port 8000

# Start frontend (in another terminal)
cd sahayak-frontend
npm run dev
```

Visit `http://localhost:5173` and test the AI features!

---

## 🚨 Common Issues & Solutions

### **Issue 1: "Authentication failed"**
**Solution:** 
- Verify `GOOGLE_APPLICATION_CREDENTIALS` path is correct
- Check service account has all required roles
- Run `gcloud auth application-default login`

### **Issue 2: "API not enabled"**
**Solution:**
- Go to Google Cloud Console > APIs & Services > Library
- Search for the specific API and enable it
- Wait 5-10 minutes for activation

### **Issue 3: "Firebase initialization failed"**
**Solution:**
- Check all Firebase environment variables are filled
- Verify project ID matches across all configs
- Ensure service account has Firebase Admin role

### **Issue 4: "Billing account required"**
**Solution:**
- Go to Google Cloud Console > Billing
- Add a payment method
- Associate billing account with your project

---

## 💰 Cost Estimation

**Google Cloud services used:**
- **Vertex AI**: ~$0.002 per 1K tokens
- **Speech-to-Text**: ~$0.016 per minute
- **Storage**: ~$0.026 per GB/month
- **Firestore**: ~$0.18 per 100K reads

**For development/testing**: ~$5-10/month
**For production**: Depends on usage

**💡 Tip**: Use Google's $300 free credits for initial development!

---

## 🎯 Next Steps

1. **Complete the setup** following all steps above
2. **Test each service** using the provided test scripts
3. **Start the application** and verify AI features work
4. **Deploy to production** when ready

**🎓 Your Sahayak AI Platform is now ready with full Google AI integration!** 