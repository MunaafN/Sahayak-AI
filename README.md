# 🚀 Sahayak AI - Hyper-Local Educational Platform

**Sahayak** is an AI-powered educational platform designed to democratize learning by providing hyper-local, multilingual educational content generation. Built with modern web technologies and powered by local AI services.

## ✨ Key Features

### 🎓 Educational Modules
- **📚 Knowledge Base** - AI-powered Q&A system for instant learning
- **📝 Lesson Planner** - Generate comprehensive lesson plans
- **📄 Content Generator** - Create educational content in multiple languages
- **📋 Worksheet Generator** - Generate practice worksheets and exercises
- **🎨 Visual Aids** - Create visual learning materials
- **📊 Reading Assessment** - Evaluate and improve reading skills

### 🌐 Multilingual Support
- Hindi, English, Bengali, Telugu, Tamil, Gujarati, Marathi, Kannada, Malayalam, Punjabi
- Real-time language switching
- Culturally appropriate content generation

### 🤖 AI-Powered Technology
- **Local AI with Ollama** (Completely Free!)
- **Google Generative AI** (Fallback option)
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
- **Ollama AI Service** (Local, Free AI)
- **Google Generative AI** (Fallback)
- **Speech Services** for TTS

## 🔧 AI Service Setup

### Option 1: Ollama AI (Recommended - Completely Free!)

1. **Install Ollama**
   ```bash
   # Windows: Download from https://ollama.ai/
   # Or use the included installer: OllamaSetup.exe
   
   # Linux/Mac:
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Pull the AI Model**
   ```bash
   ollama pull llama3:8b
   # Optional: For vision features
   ollama pull llava-phi3:latest
   ```

3. **Start Ollama Service**
   ```bash
   ollama serve
   ```

### Option 2: Google AI (Requires API Key)
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to backend `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

## 🚀 Quick Start

### Automated Setup (Windows)
```bash
python setup_sahayak.py
```

### Manual Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MunaafN/sahayak-ai.git
   cd sahayak-ai
   ```

2. **Backend Setup**
   ```bash
   cd sahayak-backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd sahayak-frontend
   npm install
   ```

4. **Start the Application**
   ```bash
   # Backend (from sahayak-backend/)
   python main.py
   
   # Frontend (from sahayak-frontend/)
   npm run dev
   ```

## 🎯 Usage

1. **Access the Platform**: Open `http://localhost:5173` in your browser
2. **Select Language**: Choose your preferred language
3. **Choose Module**: Pick from available educational modules
4. **Generate Content**: Enter your topic and get AI-generated content
5. **Listen & Learn**: Use text-to-speech for audio learning

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
│   │   ├── ollama_ai_service.py    # Local AI service
│   │   └── speech_service.py       # TTS service
│   ├── main.py               # Application entry point
│   └── requirements.txt
├── scripts/                   # Utility scripts
├── docs/                     # Documentation
└── setup_sahayak.py         # Automated setup script
```

## 🔒 Security & Privacy

- **Local AI Processing**: Ollama runs entirely on your machine
- **No Data Sharing**: Your content never leaves your system (with Ollama)
- **Secure Authentication**: Firebase-based user management
- **Open Source**: Full transparency and customization

## 🌟 Why Sahayak?

1. **100% Free AI**: Use Ollama for unlimited, free AI generation
2. **Culturally Relevant**: Content adapted for Indian educational context
3. **Multilingual**: Support for 10+ Indian languages
4. **Offline Capable**: Works without internet (with Ollama)
5. **Privacy First**: Your data stays on your machine

## 🛠️ Development

### Adding New Languages
1. Add language to `sahayak-frontend/src/config/languages.js`
2. Create translation files in `public/locales/[lang]/`
3. Update AI prompts in `ollama_ai_service.py`

### Extending AI Capabilities
1. Modify `ollama_ai_service.py` for new content types
2. Add corresponding API routes in `routers/content.py`
3. Create frontend components for new features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Ollama Team** for providing free, local AI capabilities
- **FastAPI** for the excellent Python web framework
- **React Team** for the powerful frontend library
- **Indian Education Community** for inspiration and feedback

## 📞 Support

For questions or support, please open an issue on GitHub or contact the maintainers.

---

**Built with ❤️ for democratizing education in India and beyond!**
