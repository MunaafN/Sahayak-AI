#!/usr/bin/env python3
"""
Test script to verify Ollama AI service is working with frontend inputs
"""
import asyncio
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ollama_ai_service import OllamaAIService

async def test_ai_service():
    """Test the AI service with different frontend inputs"""
    print("🧪 Testing Sahayak AI Service")
    print("=" * 50)
    
    # Initialize AI service
    service = OllamaAIService()
    
    if not service.ollama_available:
        print("❌ Ollama is not available. Please start Ollama first.")
        print("💡 Run: ollama serve")
        print("💡 Then: ollama pull llama3.1:8b")
        return False
    
    # Test cases mimicking frontend requests
    test_cases = [
        {
            "prompt": "water cycle",
            "language": "en",
            "content_type": "explanation",
            "grade_level": "3"
        },
        {
            "prompt": "Indian farmers",
            "language": "hi",
            "content_type": "story",
            "grade_level": "4"
        },
        {
            "prompt": "solar system",
            "language": "en",
            "content_type": "activity",
            "grade_level": "5"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}:")
        print(f"   Topic: {test_case['prompt']}")
        print(f"   Language: {test_case['language']}")
        print(f"   Type: {test_case['content_type']}")
        print(f"   Grade: {test_case['grade_level']}")
        print("-" * 30)
        
        try:
            response = await service.generate_text(
                test_case["prompt"],
                language=test_case["language"],
                content_type=test_case["content_type"],
                grade_level=test_case["grade_level"]
            )
            
            print(f"✅ Test {i} PASSED")
            print(f"📝 Response length: {len(response)} characters")
            
        except Exception as e:
            print(f"❌ Test {i} FAILED: {str(e)}")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! AI service is working correctly.")
    print("✅ Ready to receive requests from frontend.")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_ai_service())
    sys.exit(0 if success else 1) 