# 🚀 Sahayak AI Platform - Next Steps Guide

## 📋 Your Current Progress
✅ Google Cloud Project created  
✅ Essential APIs enabled  
❓ **You are HERE** - Ready for next steps

---

## 🔧 **Step 1: Create Service Account & Download Credentials**

### **1.1 Create Service Account**
1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Select your project**: `sahayak-ai-platform`
3. **Go to "IAM & Admin" > "Service Accounts"**
4. **Click "Create Service Account"**
5. **Fill details**:
   - **Service account name**: `sahayak-ai-service`
   - **Service account ID**: `sahayak-ai-service` (auto-filled)
   - **Description**: `Service account for Sahayak AI platform`
6. **Click "Create and Continue"**

### **1.2 Grant Permissions**
**Click "Add Role" for each of these roles**:
- `Vertex AI User`
- `Speech Editor`
- `Cloud Storage Admin`
- `Cloud Datastore User`
- `Firebase Admin`
- `Service Account Token Creator`

**Click "Continue" → "Done"**

### **1.3 Download Credentials**
1. **Click on your service account** from the list
2. **Go to "Keys" tab**
3. **Click "Add Key" → "Create new key"**
4. **Select "JSON" format**
5. **Click "Create"**
6. **Save the file** as `sahayak-credentials.json`
7. **Move the file** to your `sahayak-backend/` directory

---

## 🔥 **Step 2: Firebase Setup (FREE - No Blaze Plan Needed)**

### **2.1 Create Firebase Project**
1. **Go to Firebase Console**: https://console.firebase.google.com/
2. **Click "Add project"**
3. **Select "Use an existing Google Cloud project"**
4. **Choose your project**: `sahayak-ai-platform`
5. **Enable Google Analytics**: Choose "Yes" (recommended)
6. **Click "Create Project"**

### **2.2 Enable Authentication**
1. **Go to "Authentication"** → **"Get Started"**
2. **Go to "Sign-in method" tab**
3. **Enable Email/Password**:
   - Click "Email/Password"
   - Toggle "Enable" to ON
   - Click "Save"
4. **Enable Google Sign-In**:
   - Click "Google"
   - Toggle "Enable" to ON
   - **Project support email**: Select your email
   - Click "Save"

### **2.3 Enable Firestore Database**
1. **Go to "Firestore Database"**
2. **Click "Create database"**
3. **Choose "Start in test mode"** (FREE - No billing required)
4. **Select location**: `asia-south1 (Mumbai)`
5. **Click "Done"**

### **2.4 Enable Storage (FREE)**
1. **Go to "Storage"**
2. **Click "Get started"**
3. **Choose "Start in test mode"** (FREE - No billing required)
4. **Use same location**: `asia-south1 (Mumbai)`
5. **Click "Done"**

**✅ You get FREE**:
- 1 GB storage
- 10 GB/month transfer
- No billing required!

### **2.5 Get Firebase Web Configuration**
1. **Go to Project Settings** (⚙️ gear icon)
2. **Scroll to "Your apps" section**
3. **Click the Web icon** `</>`
4. **Register app**:
   - **App nickname**: `Sahayak Frontend`
   - **Don't check** "Also set up Firebase Hosting"
   - **Click "Register app"**
5. **Copy the configuration** (looks like this):

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC-your-api-key",
  authDomain: "sahayak-ai-platform.firebaseapp.com",
  projectId: "sahayak-ai-platform",
  storageBucket: "sahayak-ai-platform.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456789"
};
```

**Write these values down** - you'll need them for the frontend `.env` file.

---

## 🔐 **Step 3: Google OAuth Setup for Login**

### **3.1 Configure OAuth Consent Screen**
1. **Go to Google Cloud Console** → **"APIs & Services" → "OAuth consent screen"**
2. **User Type**: Select **"External"**
3. **Click "Create"**
4. **Fill App Information**:
   - **App name**: `Sahayak AI Platform`
   - **User support email**: Your email
   - **App logo**: Skip for now
   - **App domain**: Leave blank for now
   - **Developer contact**: Your email
5. **Click "Save and Continue"**
6. **Scopes**: Click "Save and Continue" (skip)
7. **Test users**: Add your email address
8. **Click "Save and Continue"**

### **3.2 Create OAuth 2.0 Client ID**
1. **Go to "APIs & Services" → "Credentials"**
2. **Click "Create Credentials" → "OAuth 2.0 Client IDs"**
3. **Application type**: **Web application**
4. **Name**: `Sahayak Frontend`
5. **Authorized JavaScript origins**: 
   - `http://localhost:5173`
   - `http://localhost:3000`
6. **Authorized redirect URIs**:
   - `http://localhost:5173`
7. **Click "Create"**
8. **Copy the Client ID** (starts with numbers, ends with `.apps.googleusercontent.com`)

---

## 📁 **Step 4: Create Environment Files**

### **4.1 Backend Environment File**
1. **Create file**: `sahayak-backend/.env`
2. **Copy content from**: `config/backend-env-template.txt`
3. **Fill in these values**:

```bash
# Generate security keys first
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

4. **Open your `sahayak-credentials.json` file** and copy these values:
   - `private_key_id` → `FIREBASE_PRIVATE_KEY_ID`
   - `private_key` → `FIREBASE_PRIVATE_KEY` (keep the quotes and \n)
   - `client_id` → `FIREBASE_CLIENT_ID`

### **4.2 Frontend Environment File**
1. **Create file**: `sahayak-frontend/.env`
2. **Copy content from**: `config/frontend-env-template.txt`
3. **Fill Firebase config values** from Step 2.5
4. **Fill Google OAuth Client ID** from Step 3.2

### **4.3 Example Backend .env File**
```bash
# Security Keys (generate these)
SECRET_KEY=your-generated-secret-key-here
JWT_SECRET_KEY=your-generated-jwt-secret-key-here

# Google Cloud
GOOGLE_CLOUD_PROJECT_ID=sahayak-ai-platform
GOOGLE_APPLICATION_CREDENTIALS=./sahayak-credentials.json

# Firebase (from sahayak-credentials.json)
FIREBASE_PROJECT_ID=sahayak-ai-platform
FIREBASE_PRIVATE_KEY_ID=a1b2c3d4e5f6
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=sahayak-ai-service@sahayak-ai-platform.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=123456789012345678901

# Demo Mode
DEMO_MODE=false
MOCK_AI_RESPONSES=false
```

### **4.4 Example Frontend .env File**
```bash
# Firebase Configuration
VITE_FIREBASE_API_KEY=AIzaSyC-your-api-key-here
VITE_FIREBASE_AUTH_DOMAIN=sahayak-ai-platform.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=sahayak-ai-platform
VITE_FIREBASE_STORAGE_BUCKET=sahayak-ai-platform.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:abcdef123456789

# Google OAuth
VITE_GOOGLE_CLIENT_ID=123456789012-abcdef.apps.googleusercontent.com

# Demo Mode
VITE_DEMO_MODE=false
```

---

## 🧪 **Step 5: Test Your Setup**

### **5.1 Install Dependencies**
```bash
# Backend
cd sahayak-backend
pip install -r requirements.txt

# Frontend
cd sahayak-frontend
npm install
```

### **5.2 Test Google Cloud Connection**
```bash
cd sahayak-backend
python -c "
import os
from google.cloud import aiplatform
from dotenv import load_dotenv

load_dotenv()
project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
location = os.getenv('GOOGLE_CLOUD_LOCATION')

try:
    aiplatform.init(project=project_id, location=location)
    print('✅ Google Cloud AI Platform connected successfully!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### **5.3 Test Firebase Connection**
```bash
cd sahayak-backend
python -c "
import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()
try:
    cred = credentials.Certificate('./sahayak-credentials.json')
    firebase_admin.initialize_app(cred)
    print('✅ Firebase connected successfully!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### **5.4 Test Speech-to-Text**
```bash
cd sahayak-backend
python -c "
from google.cloud import speech
try:
    client = speech.SpeechClient()
    print('✅ Speech-to-Text client initialized successfully!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

## 🚀 **Step 6: Start Your Application**

### **6.1 Start Backend**
```bash
cd sahayak-backend
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Start server
uvicorn main:app --reload --port 8000
```

### **6.2 Start Frontend (New Terminal)**
```bash
cd sahayak-frontend
npm run dev
```

### **6.3 Access Your Application**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🎯 **Step 7: Test Google Login**

1. **Open your app**: http://localhost:5173
2. **Click "Login" or "Sign In"**
3. **Try Google Login** - should work now!
4. **Test AI features** - should connect to real Google AI

---

## 🚨 **Troubleshooting Common Issues**

### **Issue 1: "Authentication failed"**
**Solution**:
```bash
# Reset authentication
gcloud auth revoke --all
gcloud auth login
gcloud auth application-default login
```

### **Issue 2: "Cannot find credentials file"**
**Solution**:
- Check `sahayak-credentials.json` is in `sahayak-backend/` directory
- Verify path in `.env`: `GOOGLE_APPLICATION_CREDENTIALS=./sahayak-credentials.json`

### **Issue 3: "Firebase initialization failed"**
**Solution**:
- Check all Firebase variables are filled in `.env`
- Verify `FIREBASE_PRIVATE_KEY` has proper quotes and `\n`
- Ensure service account has Firebase Admin role

### **Issue 4: "Google Sign-in not working"**
**Solution**:
- Check `VITE_GOOGLE_CLIENT_ID` is correct
- Verify OAuth consent screen is configured
- Ensure redirect URIs match your app URL

### **Issue 5: "Billing required" error**
**Solution**:
- Go to Google Cloud Console → Billing
- Add payment method (you have $300 free credits)
- Enable billing for your project

---

## 💰 **Cost Breakdown (FREE for Development)**

### **Google Cloud Free Tier**:
- **Vertex AI**: 1000 requests/month FREE
- **Speech-to-Text**: 60 minutes/month FREE
- **Cloud Storage**: 5 GB FREE
- **Firebase**: 1 GB storage + 10 GB transfer FREE
- **Total**: $0 for development!

### **After Free Tier**:
- **Vertex AI**: ~$0.002 per 1K tokens
- **Speech-to-Text**: ~$0.016 per minute
- **Storage**: ~$0.026 per GB/month
- **Expected**: $5-10/month for moderate usage

---

## 🎉 **Congratulations!**

You now have:
- ✅ **Google Cloud AI** integrated
- ✅ **Firebase Authentication** with Google Login
- ✅ **Free storage** and database
- ✅ **Real AI features** working
- ✅ **Complete development environment**

## 📞 **Need Help?**

If you encounter any issues:
1. Check the **Troubleshooting** section above
2. Verify all environment variables are filled
3. Ensure all services are enabled in Google Cloud
4. Test each component individually

**🎓 Your Sahayak AI Platform is now ready for development!** 