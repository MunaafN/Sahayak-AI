# 🚀 Sahayak AI

**Sahayak** is an AI-powered educational platform designed to democratize learning by providing hyper-local, multilingual educational content generation. Built with modern web technologies and powered by Google AI and Stability AI services.

## ✨ Key Features

### 🎓 Educational Modules
- **📚 Knowledge Base** - AI-powered Q&A system for instant learning
- **📝 Lesson Planner** - Generate comprehensive lesson plans
- **📄 Content Generator** - Create educational content in multiple languages
- **📋 Worksheet Generator** - Generate practice worksheets and exercises
- **🎨 Visual Aids** - Create high-quality visual learning materials with Stability AI
- **📊 Reading Assessment** - Evaluate and improve reading skills

### 🌐 Multilingual Support
- Hindi, English, Bengali, Telugu, Tamil, Gujarati, Marathi, Kannada, Malayalam, Punjabi
- Real-time language switching
- Culturally appropriate content generation

### 🤖 AI-Powered Technology
- **Google Generative AI (Gemini)** for intelligent content generation
- **Stability AI** for high-quality image generation (1024x1024 resolution)
- **Text-to-Speech** for accessibility
- **Intelligent content adaptation** for different grade levels

## 🏗️ Technology Stack

### Frontend
- **React 18** with Vite
- **Tailwind CSS** for styling
- **i18next** for internationalization
- **Firebase** for authentication

### Backend
- **FastAPI** (Python)
- **Google Generative AI Service** (Gemini)
- **Stability AI** for image generation
- **Speech Services** for TTS

## 🔧 AI Service Setup

### Required API Keys

#### 1. Google AI (Required)
1. Get API key from [Google AI Studio](https://ai.google.dev/)
2. Add to backend `.env` file:
   ```env
   GOOGLE_AI_API_KEY=your_google_ai_api_key_here
   ```

#### 2. Stability AI (Required for Visual Aids)
1. Get API key from [Stability AI Platform](https://platform.stability.ai/)
2. Add to backend `.env` file:
   ```env
   STABILITY_API_KEY=your_stability_ai_api_key_here
   ```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google AI API Key
- Stability AI API Key (optional, for image generation)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/sahayak-ai.git
cd sahayak-ai
```

### 2. Backend Setup
```bash
cd sahayak-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
# Copy from config/backend-env-template.txt
```

### 3. Frontend Setup
```bash
cd sahayak-frontend
npm install

# Create .env file for frontend
# Copy from config/frontend-env-template.txt
```

### 4. Start the Application
```bash
# Backend (from sahayak-backend/)
python main.py

# Frontend (from sahayak-frontend/ in a new terminal)
npm run dev
```

### 5. Access the Platform
Open `http://localhost:5173` in your browser

## 🧪 Testing

### Test Google AI Integration
```bash
cd sahayak-backend
python test_google_ai.py
```

### Test Stability AI Integration
```bash
cd sahayak-backend
python test_stability_ai.py
```

### Test via Browser
- Backend health: `http://localhost:8000/health`
- Stability AI test: `http://localhost:8000/visuals/test-stability`

## 🎯 Usage

1. **Access the Platform**: Open `http://localhost:5173` in your browser
2. **Select Language**: Choose your preferred language
3. **Choose Module**: Pick from available educational modules
4. **Generate Content**: Enter your topic and get AI-generated content
5. **Listen & Learn**: Use text-to-speech for audio learning
6. **Create Visuals**: Generate educational images with Stability AI

## 📁 Project Structure

```
sahayak-ai/
├── sahayak-frontend/          # React frontend application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── config/           # Configuration files
│   │   └── utils/            # Utility functions
│   └── package.json
├── sahayak-backend/           # FastAPI backend
│   ├── routers/              # API route handlers
│   ├── services/             # AI and external services
│   │   ├── genkit_ai_service.py    # Google AI service
│   │   └── speech_service.py       # TTS service
│   ├── main.py               # Application entry point
│   └── requirements.txt
├── scripts/                   # Utility scripts
├── config/                   # Configuration templates
├── docs/                     # Documentation
└── MIGRATION_COMPLETE.md     # Migration details
```

## 💰 Cost Information

### Google AI (Gemini)
- **Free Tier**: 15 requests/minute, 1500 requests/day
- **Typical Cost**: $0-15/month for educational usage
- [Pricing Details](https://ai.google.dev/pricing)

### Stability AI
- **Cost**: ~$0.040 per image (1024x1024)
- **Recommended**: Start with $10 credit
- [Pricing Details](https://platform.stability.ai/pricing)

## 🔒 Security & Privacy

- **API Key Security**: Never commit API keys to version control
- **Environment Variables**: Use `.env` files for sensitive data
- **Secure Authentication**: Firebase-based user management
- **Open Source**: Full transparency and customization

## 🌟 Why Sahayak?

1. **High-Quality AI**: Google Gemini for superior content generation
2. **Professional Images**: Stability AI for educational visuals
3. **Culturally Relevant**: Content adapted for Indian educational context
4. **Multilingual**: Support for 10+ Indian languages
5. **Modern Architecture**: Built with latest web technologies

## 🛠️ Development

### Adding New Languages
1. Add language to `sahayak-frontend/src/config/languages.js`
2. Create translation files in `public/locales/[lang]/`
3. Update AI prompts in `genkit_ai_service.py`

### Extending AI Capabilities
1. Modify `genkit_ai_service.py` for new content types
2. Add corresponding API routes in `routers/`
3. Create frontend components for new features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Google AI Team** for providing excellent Generative AI capabilities
- **Stability AI** for state-of-the-art image generation
- **FastAPI** for the excellent Python web framework
- **React Team** for the powerful frontend library
- **Indian Education Community** for inspiration and feedback

## 📞 Support

For questions or support, please:
1. Check the documentation in `docs/` folder
2. Review setup guides in `config/` folder
3. Open an issue on GitHub
4. Contact the maintainers

---

**Built with ❤️ for democratizing education in India and beyond!**
