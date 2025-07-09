# 🔑 Environment Variables Reference Card

## 📋 Quick Checklist

### ✅ Required for AI Features
- [ ] `GOOGLE_CLOUD_PROJECT_ID` - Your Google Cloud project ID
- [ ] `GOOGLE_APPLICATION_CREDENTIALS` - Path to service account JSON file
- [ ] `FIREBASE_PROJECT_ID` - Firebase project ID (usually same as GCP)
- [ ] `FIREBASE_PRIVATE_KEY` - Firebase service account private key
- [ ] `FIREBASE_CLIENT_EMAIL` - Firebase service account email

### 🔧 Optional but Recommended
- [ ] `OPENAI_API_KEY` - OpenAI API key (fallback for AI features)
- [ ] `SECRET_KEY` - Application secret key (generate random string)
- [ ] `JWT_SECRET_KEY` - JWT signing secret (generate random string)

### 🎯 Demo Mode (Default)
- [ ] `DEMO_MODE=true` - Enables demo mode without AI services
- [ ] `MOCK_AI_RESPONSES=true` - Uses mock responses instead of real AI

---

## 🗂️ Complete Environment Variables List

### 🔙 Backend Environment (`.env` in `sahayak-backend/`)

```bash
# ================================
# CORE APPLICATION SETTINGS
# ================================
APP_NAME=Sahayak AI Platform
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# ================================
# GOOGLE CLOUD CONFIGURATION
# ================================
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Vertex AI Models
VERTEX_AI_ENDPOINT=us-central1-aiplatform.googleapis.com
VERTEX_AI_TEXT_MODEL=gemini-pro
VERTEX_AI_VISION_MODEL=gemini-pro-vision
VERTEX_AI_IMAGE_MODEL=imagegeneration@002

# Speech Services
SPEECH_API_ENDPOINT=speech.googleapis.com
SPEECH_LANGUAGE_CODES=en-US,hi-IN,mr-IN

# ================================
# FIREBASE CONFIGURATION
# ================================
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=service-account@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/service-account%40project.iam.gserviceaccount.com

# ================================
# DATABASE & STORAGE
# ================================
DATABASE_URL=sqlite:///./sahayak.db
GOOGLE_CLOUD_STORAGE_BUCKET=your-project-storage
UPLOAD_MAX_SIZE=10485760
ALLOWED_FILE_TYPES=jpg,jpeg,png,gif,pdf,doc,docx,mp3,wav,ogg

# ================================
# AI SERVICES
# ================================
OPENAI_API_KEY=your-openai-api-key-optional
OPENAI_MODEL=gpt-3.5-turbo
MAX_CONTENT_LENGTH=2000
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=1000

# ================================
# PERFORMANCE & CACHING
# ================================
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# ================================
# SECURITY & NETWORKING
# ================================
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=*
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# ================================
# EMAIL NOTIFICATIONS
# ================================
EMAIL_BACKEND=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_USE_TLS=true

# ================================
# MONITORING & LOGGING
# ================================
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn-optional

# ================================
# DEMO/DEVELOPMENT MODE
# ================================
DEMO_MODE=true
MOCK_AI_RESPONSES=true
```

### 🎨 Frontend Environment (`.env` in `sahayak-frontend/`)

```bash
# ================================
# FIREBASE CONFIGURATION
# ================================
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:abcdef123456789
VITE_FIREBASE_MEASUREMENT_ID=G-ABCDEFGHIJ

# ================================
# API CONFIGURATION
# ================================
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# ================================
# APPLICATION SETTINGS
# ================================
VITE_APP_NAME=Sahayak
VITE_APP_VERSION=1.0.0
VITE_ENVIRONMENT=development

# ================================
# FEATURE FLAGS
# ================================
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_ERROR_REPORTING=true
VITE_ENABLE_VOICE_FEATURES=true
VITE_ENABLE_OFFLINE_MODE=false

# ================================
# UI CONFIGURATION
# ================================
VITE_DEFAULT_LANGUAGE=en
VITE_SUPPORTED_LANGUAGES=en,hi,mr
VITE_THEME=light

# ================================
# DEMO MODE
# ================================
VITE_DEMO_MODE=true
VITE_SHOW_DEMO_DATA=true
```

---

## 🔧 How to Get These Values

### 🌐 Google Cloud Values

1. **Create Google Cloud Project**:
   ```bash
   gcloud projects create your-project-id
   gcloud config set project your-project-id
   ```

2. **Get Project ID**:
   ```bash
   gcloud config get-value project
   ```

3. **Create Service Account & Download Credentials**:
   ```bash
   gcloud iam service-accounts create sahayak-ai-service
   gcloud iam service-accounts keys create credentials.json \
     --iam-account=sahayak-ai-service@your-project-id.iam.gserviceaccount.com
   ```

### 🔥 Firebase Values

1. **Go to [Firebase Console](https://console.firebase.google.com/)**
2. **Select your project**
3. **Go to Project Settings (⚙️ icon)**
4. **Scroll to "Your apps" section**
5. **Click "Add app" → Web**
6. **Copy the config object values**

### 🔑 Security Keys (Generate Random Strings)

```bash
# Generate secret keys (Linux/Mac)
openssl rand -hex 32

# Generate secret keys (Python - any OS)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 📧 Email Configuration

1. **For Gmail**:
   - Enable 2-factor authentication
   - Generate App Password
   - Use App Password as `SMTP_PASSWORD`

---

## 🚀 Quick Start Commands

### 1. Start with Demo Mode (No AI Setup Required)
```bash
# Backend .env
DEMO_MODE=true
MOCK_AI_RESPONSES=true

# Frontend .env  
VITE_DEMO_MODE=true
```

### 2. Enable Real AI Features
```bash
# Backend .env
DEMO_MODE=false
MOCK_AI_RESPONSES=false
GOOGLE_CLOUD_PROJECT_ID=your-actual-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json

# Frontend .env
VITE_DEMO_MODE=false
VITE_FIREBASE_API_KEY=your-actual-firebase-key
```

### 3. Test Configuration
```bash
# Test backend
cd sahayak-backend
python setup_ai.py --test

# Test frontend
cd sahayak-frontend
npm run build
```

---

## 🆘 Troubleshooting

### ❌ Common Issues

1. **"Firebase not initialized"**
   - Check `VITE_FIREBASE_API_KEY` and other Firebase config
   - Ensure Firebase project exists and is active

2. **"Google Cloud authentication failed"**
   - Verify `GOOGLE_APPLICATION_CREDENTIALS` path
   - Check service account has proper roles
   - Run `gcloud auth application-default login`

3. **"CORS errors"**
   - Update `ALLOWED_ORIGINS` in backend .env
   - Ensure frontend URL matches

4. **"AI responses not working"**
   - Check `DEMO_MODE` and `MOCK_AI_RESPONSES` settings
   - Verify Google Cloud APIs are enabled
   - Test with `python setup_ai.py --test`

### ✅ Quick Fixes

```bash
# Reset Google Cloud auth
gcloud auth revoke --all
gcloud auth login
gcloud auth application-default login

# Regenerate Firebase config
# Visit Firebase Console → Project Settings → General

# Test environment loading
cd sahayak-backend
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✅ Env loaded')"
```

---

## 📱 Ready to Deploy?

When moving to production, remember to:

- [ ] Change all `your-*` placeholders to real values
- [ ] Set `DEBUG=false` and `ENVIRONMENT=production`
- [ ] Use strong, unique secret keys
- [ ] Enable HTTPS and update CORS settings
- [ ] Set up proper database (PostgreSQL)
- [ ] Configure monitoring and logging
- [ ] Enable Firebase security rules
- [ ] Set up proper backup and recovery

**🎓 Happy coding with Sahayak AI Platform!** 