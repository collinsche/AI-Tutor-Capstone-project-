#!/usr/bin/env python3
"""
Simple API Key Test for AI Educational Assistant
Tests the OpenAI API key with a basic request
"""

import os
from dotenv import load_dotenv

def test_api_key():
    """Test the OpenAI API key with a simple request"""
    print("🚀 Testing OpenAI API Key")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    if api_key == "your_openai_api_key_here":
        print("❌ API key is still the placeholder value")
        return False
    
    print(f"🔑 API Key found: {api_key[:10]}...{api_key[-10:]}")
    
    try:
        from openai import OpenAI
        
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        # Test with a simple completion
        print("🌐 Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello, API test successful!'"}
            ],
            max_tokens=50
        )
        
        if response.choices:
            message = response.choices[0].message.content
            print(f"✅ API Test Successful!")
            print(f"📝 Response: {message}")
            return True
        else:
            print("❌ No response received from API")
            return False
            
    except Exception as e:
        print(f"❌ API Test Failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api_key()
    if success:
        print("\n🎉 Your OpenAI API key is working correctly!")
        print("🚀 You can now use the full AI Educational Assistant features.")
    else:
        print("\n⚠️  API key test failed. Please check your configuration.")