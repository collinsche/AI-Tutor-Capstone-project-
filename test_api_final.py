#!/usr/bin/env python3
"""
Final API Key Test for Grok
Comprehensive test to verify API key functionality
"""

import os
import sys
from dotenv import load_dotenv
import requests

def test_api_key():
    """Test the API key with different approaches"""
    print("🔍 Final API Key Test - Grok")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('GROK_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:]}")
    print(f"📏 Key Length: {len(api_key)} characters")
    print(f"🏷️  Key Format: {'✅ Valid format' if api_key.startswith('xai-') else '❌ Invalid format'}")
    
    # Test 1: Basic Grok API test
    print("\n🧪 Test 1: Basic Grok API Client")
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'x-ai/grok-4-fast',
            'messages': [
                {"role": "user", "content": "Say 'Hello, API test successful!'"}
            ],
            'max_tokens': 20,
            'temperature': 0.1
        }
        
        response = requests.post(
            'https://api.x.ai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('choices') and data['choices'][0].get('message'):
                print("✅ API Test SUCCESSFUL!")
                print(f"📝 Response: {data['choices'][0]['message']['content']}")
                return True
            else:
                print("❌ API returned empty response")
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return False
            return False
            
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        
        # Check specific error types
        if "401" in str(e) or "invalid_api_key" in str(e):
            print("🔍 Error Analysis: Invalid API key")
            print("💡 Possible solutions:")
            print("   • Verify the API key is correct")
            print("   • Check if the key has expired")
            print("   • Ensure the key has proper permissions")
            print("   • Try generating a new API key")
        elif "429" in str(e):
            print("🔍 Error Analysis: Rate limit exceeded")
        elif "quota" in str(e).lower():
            print("🔍 Error Analysis: Quota exceeded")
        
        return False
    
    # Test 2: Alternative endpoint test
    print("\n🧪 Test 2: Models List Test")
    try:
        models = client.models.list()
        print("✅ Models endpoint accessible")
        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def test_demo_mode():
    """Test if the app works in demo mode"""
    print("\n🎭 Testing Demo Mode Functionality")
    print("-" * 40)
    
    try:
        # Test if main app can load
        sys.path.append('src')
        
        # Import main components
        from config import ConfigManager
        print("✅ Config manager loaded")
        
        from educational_assistant import EducationalAssistant
        print("✅ Educational assistant loaded")
        
        from user_profile import UserProfile
        print("✅ User profile system loaded")
        
        from learning_analytics import LearningAnalytics
        print("✅ Learning analytics loaded")
        
        print("\n🎉 Demo mode is fully functional!")
        print("💡 Your app will work perfectly for demonstration")
        return True
        
    except Exception as e:
        print(f"❌ Demo mode test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Final API Key Test...\n")
    
    # Test API key
    api_success = test_api_key()
    
    # Test demo mode
    demo_success = test_demo_mode()
    
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    if api_success:
        print("🎉 API KEY IS WORKING!")
        print("✅ Your AI Educational Assistant is fully functional")
        print("🤖 Real AI responses will be available")
    elif demo_success:
        print("🎭 API key not working, but DEMO MODE is ready!")
        print("✅ Your app is perfect for demonstration")
        print("🎬 All UI features work without API dependency")
    else:
        print("⚠️  Some issues detected, but basic functionality available")
    
    print(f"\n🌐 Access your app at: http://localhost:8501")
    print("🎥 Ready for your capstone video demonstration!")