# 🔍 Llava-Phi3 Vision-Based Worksheet Generation

## Overview

The worksheet generation feature now uses **llava-phi3**, a powerful vision-language model that can analyze textbook page images and generate educational content based on what it sees. This creates more accurate and contextually relevant worksheets.

## How It Works

### 1. Vision Analysis
- Llava-phi3 analyzes the uploaded textbook page image
- Identifies text, diagrams, charts, and educational content
- Understands the context and subject matter

### 2. Intelligent Worksheet Generation
- Combines visual analysis with your inputs (subject, grade levels)
- Creates grade-appropriate questions and exercises
- Generates diverse question types (multiple choice, fill-in-the-blank, short answer)
- Follows Indian curriculum standards

## Setup Instructions

### Prerequisites
- Ollama must be installed and running
- Internet connection for initial model download

### Installation Steps

1. **Install Llava-Phi3 Model**
   ```bash
   ollama pull llava-phi3
   ```

2. **Or Run the Setup Script**
   ```bash
   # Windows
   scripts/start-llava-phi3.bat
   ```

3. **Verify Installation**
   ```bash
   ollama list
   # Should show llava-phi3 in the list
   ```

## Features

### 🎯 Vision-Based Analysis
- Reads text content from textbook pages
- Analyzes diagrams, charts, and illustrations  
- Understands mathematical formulas and equations
- Identifies key concepts and topics

### 📚 Multi-Grade Support
- Generates differentiated content for multiple grade levels
- Adjusts complexity based on target grade
- Creates age-appropriate questions and activities

### 🔄 Automatic Model Management
- Backend automatically starts llava-phi3 when needed
- Handles model loading and API communication
- Provides graceful fallbacks for errors

### 📊 Comprehensive Question Types
- Multiple choice questions
- Fill-in-the-blank exercises
- Short answer questions
- Problem-solving activities
- Matching exercises

## Usage

### In the Worksheet Generator:

1. **Upload Image**: Select a textbook page image
2. **Choose Subject**: Select the relevant subject area
3. **Select Grades**: Pick target grade levels (can select multiple)
4. **Generate**: Click "Generate Worksheets"

### Sample Workflow:
```
1. Upload: Math textbook page showing fractions
2. Subject: Mathematics  
3. Grades: 4, 5
4. Result: Grade-specific fraction worksheets with:
   - Visual fraction problems
   - Word problems based on textbook examples
   - Practice exercises matching the content level
```

## Technical Implementation

### Backend Architecture
```
📁 sahayak-backend/routers/worksheets.py
├── /generate (original endpoint - still works)
└── /generate-with-vision (new llava-phi3 endpoint)
```

### API Flow
1. **Image Processing**: Convert base64 image for llava-phi3
2. **Model Start**: Ensure llava-phi3 is running via Ollama
3. **Prompt Creation**: Combine image + text inputs into natural sentence
4. **Vision Analysis**: Send to llava-phi3 via Ollama API
5. **Content Generation**: Receive and format worksheet content
6. **Response**: Return grade-specific worksheets

### Sample API Request
```json
POST /worksheets/generate-with-vision
{
  "image": "data:image/jpeg;base64,/9j/4AAQ...", 
  "grades": ["4", "5"],
  "subject": "Mathematics"
}
```

### Sample Sentence Prompt
```
"I am looking at a textbook page image for Mathematics subject, 
and I need to create educational worksheet activities for grade 4 students. 
Please analyze this image and generate appropriate worksheet content 
including questions, exercises, and activities based on what you can 
see in the textbook page. Make it suitable for Indian curriculum 
standards and include diverse question types like fill-in-the-blank, 
multiple choice, short answers, and practice problems."
```

## Error Handling

### Graceful Fallbacks
- Timeout handling (120 seconds per worksheet)
- Model unavailability warnings
- Connection error recovery
- Empty response handling

### Status Messages
- ✅ Success: "Generated worksheet for Grade X"
- ⏱️ Timeout: "Generation timed out. Please try again."
- ❌ Error: "API error 500 for Grade X"
- ⚠️ Warning: "Model start timeout, proceeding anyway..."

## Troubleshooting

### Common Issues

1. **"Model not found" Error**
   ```bash
   # Solution: Install the model
   ollama pull llava-phi3
   ```

2. **Timeout Errors**
   - First run takes longer (model loading)
   - Large images may take more time
   - Try smaller image files

3. **Connection Refused**
   ```bash
   # Ensure Ollama is running
   ollama serve
   ```

4. **Poor Quality Output**
   - Use clear, high-contrast images
   - Ensure text is readable in the uploaded image
   - Try different image angles or crops

### Model Information
- **Model**: llava-phi3
- **Size**: ~2.9GB download
- **Requirements**: 8GB+ RAM recommended
- **API**: Ollama REST API (localhost:11434)

## Advantages Over Traditional Generation

### Before (Text-only)
- Generic worksheet templates
- No connection to specific textbook content
- Limited context understanding

### After (Vision-enabled)
- Analyzes actual textbook content
- Creates questions based on visible material
- Understands diagrams and illustrations
- More relevant and contextual worksheets

## Future Enhancements

- Support for multiple image uploads
- OCR text extraction for better accuracy
- Template-based formatting options
- Integration with assessment tools
- Multilingual vision analysis

---

**Note**: This feature requires Ollama and the llava-phi3 model. The first generation may take longer as the model loads into memory. 