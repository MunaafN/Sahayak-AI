# 🔧 Complete Environment Setup for Genkit AI

## 📋 Backend Environment (.env file)

Create `sahayak-backend/.env` with this content:

```env
# ================================
# SAHAYAK BACKEND CONFIGURATION
# ================================

# 🤖 GOOGLE AI API KEY (REQUIRED)
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# 🔐 SECURITY KEYS
SECRET_KEY=your-secret-key-for-production
JWT_SECRET=your-jwt-secret-for-tokens
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# 🌐 CORS SETTINGS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=*

# 📊 APPLICATION SETTINGS
DEMO_MODE=false
ENVIRONMENT=development

# 🗄️ DATABASE (optional)
DATABASE_URL=sqlite:///sahayak.db

# ☁️ GOOGLE CLOUD (optional - for advanced features)
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=./sahayak-credentials.json
```

## 📋 Frontend Environment (.env file)

Create `sahayak-frontend/.env` with this content:

```env
# ================================
# SAHAYAK FRONTEND CONFIGURATION
# ================================

# 🔥 FIREBASE CONFIGURATION
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abcdef123456

# 🔗 BACKEND API
VITE_API_BASE_URL=http://localhost:8000

# 🌐 APPLICATION SETTINGS
VITE_APP_NAME=Sahayak AI
VITE_APP_VERSION=1.0.0
VITE_ENVIRONMENT=development
```

## 🔑 How to Get API Keys

### 📱 Google AI API Key (Required)
1. Visit: https://ai.google.dev/
2. Click "Get API key in Google AI Studio"
3. Sign in with your Google account
4. Click "Create API key"
5. Copy the key (starts with 'AIza...')
6. Paste in backend .env: `GOOGLE_AI_API_KEY=AIza...`

### 🔥 Firebase API Keys (Required for Auth)
1. Visit: https://console.firebase.google.com/
2. Create a new project or select existing
3. Go to Project Settings > General
4. Scroll to "Your apps" and click "Web app"
5. Copy the config values to frontend .env

## ✅ Verification

### Test Backend:
```bash
cd sahayak-backend
python -c "from services.genkit_ai_service import GenkitAIService; service = GenkitAIService(); print('✅ Google AI working!' if service.genkit_available else '❌ Check API key')"
```

### Test Frontend:
```bash
cd sahayak-frontend
npm run dev
```

## 🚀 Benefits of This Setup

✅ **Better Hindi Grammar** - Google Gemini excels at Hindi content
✅ **Faster Responses** - Direct Google AI integration
✅ **No Ollama Required** - Simplified dependency management
✅ **Free Tier** - Generous Google AI free usage
✅ **Better Accuracy** - Superior factual content generation
✅ **Stable** - No complex framework dependencies

## 💰 Cost Breakdown

- **Google AI API**: FREE tier (15 requests/minute, 1500 requests/day)
- **Firebase Auth**: FREE tier (up to 10,000 monthly active users)
- **Typical Monthly Cost**: $0-15 for educational usage

## 🔧 Troubleshooting

### If AI generation fails:
1. Check API key is correctly set in .env
2. Ensure internet connection
3. Verify API key has permissions
4. Check console for error messages

### If frontend login fails:
1. Verify Firebase config in frontend .env
2. Check Firebase console for auth settings
3. Ensure domains are added to Firebase auth 