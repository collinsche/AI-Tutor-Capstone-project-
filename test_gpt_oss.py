#!/usr/bin/env python3
"""
GPT-OSS-120B API Key Test for AI Educational Assistant
Tests the OpenAI API key specifically for GPT-OSS-120B model
"""

import os
from dotenv import load_dotenv

def test_gpt_oss_api():
    """Test the OpenAI API key with GPT-OSS-120B model"""
    print("🚀 Testing GPT-OSS-120B API Key")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('AI_MODEL', 'gpt-oss-120b')
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    print(f"🔑 API Key: {api_key[:15]}...{api_key[-10:]}")
    print(f"🤖 Model: {model}")
    
    try:
        from openai import OpenAI
        
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        # Test with GPT-OSS-120B model
        print("🌐 Testing GPT-OSS-120B connection...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Hello! Please confirm you are GPT-OSS-120B and working correctly."}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        if response.choices:
            message = response.choices[0].message.content
            print(f"✅ GPT-OSS-120B Test Successful!")
            print(f"📝 Response: {message}")
            
            # Test educational assistant functionality
            print("\n🎓 Testing Educational Assistant Integration...")
            edu_response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an AI educational assistant. Help students learn effectively."},
                    {"role": "user", "content": "Explain photosynthesis in simple terms."}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            if edu_response.choices:
                edu_message = edu_response.choices[0].message.content
                print(f"✅ Educational Assistant Test Successful!")
                print(f"📚 Educational Response: {edu_message[:100]}...")
                return True
            
        return False
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ API Test Failed: {error_msg}")
        
        # Provide specific guidance for different error types
        if "invalid_api_key" in error_msg.lower():
            print("\n💡 Troubleshooting:")
            print("   • Verify your API key is correct")
            print("   • Check if the key is specifically for GPT-OSS-120B")
            print("   • Ensure your account has access to this model")
        elif "model" in error_msg.lower():
            print("\n💡 Model Issue:")
            print("   • GPT-OSS-120B might not be available")
            print("   • Try with a different model name")
            print("   • Check model availability in your account")
        
        return False

if __name__ == "__main__":
    success = test_gpt_oss_api()
    if success:
        print("\n🎉 Your GPT-OSS-120B API key is working correctly!")
        print("🚀 The AI Educational Assistant is ready with full functionality.")
    else:
        print("\n⚠️  API key test failed. Please check your configuration.")
        print("🔧 Make sure your API key is valid for GPT-OSS-120B model.")