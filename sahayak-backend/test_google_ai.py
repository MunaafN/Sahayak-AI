#!/usr/bin/env python3
"""
Test Google AI service after Ollama removal
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_google_ai():
    """Test Google AI service functionality"""
    try:
        from services.genkit_ai_service import GenkitAIService
        
        print("🧪 Testing Google AI Service...")
        print("=" * 50)
        
        # Initialize service
        service = GenkitAIService()
        
        if not service.genkit_available:
            print("❌ Google AI is not available.")
            print("💡 Please add GOOGLE_AI_API_KEY to .env file")
            print("📖 Get API key from: https://ai.google.dev/")
            return False
        
        print("✅ Google AI service initialized!")
        print()
        
        # Test Hindi content generation
        print("🇮🇳 Testing Hindi Content Generation...")
        hindi_content = await service.generate_text(
            "सूर्य के बारे में",
            language="hi",
            content_type="explanation",
            grade_level="3",
            length="short"
        )
        print(f"✅ Hindi Response: {hindi_content[:100]}...")
        print()
        
        # Test English content generation
        print("🇺🇸 Testing English Content Generation...")
        english_content = await service.generate_text(
            "The Solar System",
            language="en",
            content_type="explanation", 
            grade_level="3",
            length="short"
        )
        print(f"✅ English Response: {english_content[:100]}...")
        print()
        
        print("🎉 All tests passed! Google AI service is working perfectly.")
        print("=" * 50)
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔥 Google AI Service Test")
    print("🗑️ Ollama has been completely removed")
    print("🚀 Testing new Google AI integration...")
    print()
    
    success = asyncio.run(test_google_ai())
    
    if success:
        print("\n✅ Setup Complete! You can now:")
        print("   1. Run: python main.py")
        print("   2. Visit: http://localhost:8000")
        print("   3. Test AI features in the frontend")
    else:
        print("\n❌ Setup needs attention:")
        print("   1. Add Google AI API key to .env")
        print("   2. Run this test again")
        print("   3. Check the setup guide") 