#!/usr/bin/env python3
"""
Test script for Stability AI integration in Sahayak AI Platform
"""

import os
import sys
import requests
import base64
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_stability_ai():
    """Test Stability AI image generation"""
    print("🧪 TESTING STABILITY AI INTEGRATION")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        print("❌ STABILITY_API_KEY not found in environment")
        print("💡 Add your API key to .env file:")
        print("   STABILITY_API_KEY=sk-your-api-key-here")
        return False
    
    if api_key == "your-stability-ai-api-key-here":
        print("❌ STABILITY_API_KEY is still the template value")
        print("💡 Replace with your actual API key from https://platform.stability.ai/")
        return False
    
    print(f"✅ API Key found: {api_key[:15]}...")
    
    # Test API connectivity
    print("\n🔗 Testing API connectivity...")
    
    try:
        # Test with simple educational prompt
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        
        test_prompt = """
        Educational illustration of a simple red apple, high quality, detailed, vibrant colors, 
        child-friendly, classroom appropriate, professional educational material, 
        clear visual elements, engaging design, suitable for learning, 
        digital art, clean composition, educational illustration, safe for children
        """
        
        payload = {
            "text_prompts": [
                {
                    "text": test_prompt.strip(),
                    "weight": 1
                },
                {
                    "text": "blurry, low quality, inappropriate, violent, scary, dark, adult content, nsfw",
                    "weight": -1
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "steps": 30,
            "samples": 1,
            "style_preset": "digital-art"
        }
        
        print("📝 Test prompt: Educational red apple illustration")
        print("⏳ Generating image (this may take 30-60 seconds)...")
        
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        generation_time = time.time() - start_time
        
        print(f"⏱️ Generation took {generation_time:.1f} seconds")
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Image generation successful!")
            
            data = response.json()
            if "artifacts" in data and len(data["artifacts"]) > 0:
                # Save test image
                image_data = data["artifacts"][0]
                image_base64 = image_data.get("base64")
                
                if image_base64:
                    # Create uploads directory
                    os.makedirs("uploads/test", exist_ok=True)
                    
                    # Save image
                    filename = f"stability_test_{int(time.time())}.png"
                    filepath = os.path.join("uploads/test", filename)
                    
                    image_bytes = base64.b64decode(image_base64)
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                    
                    print(f"🖼️ Test image saved: {filepath}")
                    print(f"📏 Image size: {len(image_bytes)} bytes")
                    
                    return True
                else:
                    print("⚠️ No image data in response")
                    return False
            else:
                print("⚠️ No artifacts in response")
                print(f"📄 Response: {response.text[:200]}")
                return False
                
        elif response.status_code == 401:
            print("❌ Authentication failed")
            print("💡 Check your API key is correct and active")
            return False
        elif response.status_code == 402:
            print("💳 Insufficient credits")
            print("💡 Add credits to your Stability AI account")
            return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out")
        print("💡 Try again - image generation can take time")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🎨 SAHAYAK AI - STABILITY AI TEST")
    print("=" * 60)
    
    success = test_stability_ai()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ STABILITY AI INTEGRATION TEST PASSED!")
        print("🎉 Your image generation system is ready!")
        print("\n📋 Next steps:")
        print("1. Start the backend: python main.py")
        print("2. Test in browser: http://localhost:8000/visuals/test-stability")
        print("3. Try the visual aids feature in the frontend")
    else:
        print("❌ STABILITY AI INTEGRATION TEST FAILED!")
        print("\n🔧 Troubleshooting:")
        print("1. Check your API key is correct")
        print("2. Verify account has sufficient credits")
        print("3. Check internet connectivity")
        print("4. Review setup instructions in config/stability-ai-setup-instructions.txt")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 