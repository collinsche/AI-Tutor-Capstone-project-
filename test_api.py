#!/usr/bin/env python3
"""
API Key Testing Script
Tests the functionality of configured API keys for the AI Educational Assistant using Grok
"""

import os
import sys
from dotenv import load_dotenv
import requests

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    return {
        'api_key': os.getenv('GROK_API_KEY'),
        'model': os.getenv('AI_MODEL', 'x-ai/grok-4-fast'),
        'temperature': float(os.getenv('AI_TEMPERATURE', '0.7')),
        'max_tokens': int(os.getenv('AI_MAX_TOKENS', '1000'))
    }

def test_api_key_format(api_key):
    """Test if API key has the correct format"""
    print("🔍 Testing API Key Format...")
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    if api_key == "your_openai_api_key_here":
        print("❌ API key is still the placeholder value")
        print("   Please replace 'your_openai_api_key_here' with your actual OpenAI API key")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ API key doesn't start with 'sk-' (invalid format)")
        return False
    
    if len(api_key) < 20:
        print("❌ API key appears to be too short")
        return False
    
    print("✅ API key format appears valid")
    return True

def test_grok_connection(config):
    """Test connection to Grok API via OpenRouter"""
    print("\n🌐 Testing Grok API Connection via OpenRouter...")
    
    try:
        # Prepare headers and payload for OpenRouter API
        headers = {
            'Authorization': f'Bearer {config["api_key"]}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://localhost:8502',  # Optional for OpenRouter
            'X-Title': 'AI Educational Assistant'  # Optional for OpenRouter
        }
        
        payload = {
            'model': config['model'],
            'messages': [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API test successful' if you can read this."}
            ],
            'max_tokens': 50,
            'temperature': 0.1
        }
        
        # Make request to OpenRouter API
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('choices') and data['choices'][0].get('message'):
                message = data['choices'][0]['message']['content'].strip()
                print(f"✅ Grok API connection successful via OpenRouter!")
                print(f"   Response: {message}")
                print(f"   Model used: {config['model']}")
                print(f"   Tokens used: {data.get('usage', {}).get('total_tokens', 'N/A')}")
                return True
            else:
                print("❌ Received empty response from Grok API")
                return False
        else:
            print(f"❌ Grok API error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_educational_assistant_integration():
    """Test integration with the educational assistant"""
    print("\n🎓 Testing Educational Assistant Integration...")
    
    try:
        # Import the educational assistant
        sys.path.append('src')
        from educational_assistant import EducationalAssistant
        
        # Initialize the assistant
        assistant = EducationalAssistant()
        
        # Test a simple educational query with proper user profile
        test_query = "Explain what 2+2 equals in simple terms"
        user_profile = {
            'name': 'Test User',
            'learning_style': 'Visual',
            'grade_level': 'Elementary',
            'subjects': ['Math']
        }
        response = assistant.generate_response(test_query, user_profile)
        
        if response and len(response.strip()) > 0:
            print("✅ Educational Assistant integration successful!")
            print(f"   Test query: {test_query}")
            print(f"   Response preview: {response[:100]}...")
            return True
        else:
            print("❌ Educational Assistant returned empty response")
            return False
            
    except ImportError as e:
        print(f"❌ Could not import Educational Assistant: {e}")
        return False
    except Exception as e:
        print(f"❌ Educational Assistant test failed: {e}")
        return False

def main():
    """Main testing function"""
    print("🚀 AI Educational Assistant - API Key Testing")
    print("=" * 50)
    
    # Load configuration
    config = load_environment()
    
    # Test API key format
    if not test_api_key_format(config['api_key']):
        print("\n❌ API key format test failed. Please fix the issues above.")
        return False
    
    # Test Grok connection
    if not test_grok_connection(config):
        print("\n❌ Grok API connection test failed. Please check your API key and internet connection.")
        return False
    
    # Test educational assistant integration
    if not test_educational_assistant_integration():
        print("\n⚠️  Educational Assistant integration test failed, but API key is working.")
        print("   This might be due to missing dependencies or configuration issues.")
    
    print("\n" + "=" * 50)
    print("🎉 API Key Testing Complete!")
    print("✅ Your OpenAI API key is properly configured and functional.")
    print("🚀 You can now use the AI Educational Assistant with full functionality.")
    
    return True

if __name__ == "__main__":
    main()