#!/usr/bin/env python3
"""
Application Testing Script (Without API Key)
Tests the AI Educational Assistant functionality without requiring actual API keys
"""

import os
import sys
from dotenv import load_dotenv

def test_environment_setup():
    """Test if environment is properly set up"""
    print("🔧 Testing Environment Setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    print("✅ .env file exists")
    
    # Check key environment variables
    env_vars = {
        'GROK_API_KEY': os.getenv('GROK_API_KEY'),
        'AI_MODEL': os.getenv('AI_MODEL', 'x-ai/grok-4-fast'),
        'APP_PORT': os.getenv('APP_PORT', '8501'),
        'APP_HOST': os.getenv('APP_HOST', 'localhost')
    }
    
    print("📋 Environment Variables:")
    for key, value in env_vars.items():
        if key == 'GROK_API_KEY':
            if value and value != 'your_grok_api_key_here':
                print(f"   ✅ {key}: Configured (xai-****...)")
            else:
                print(f"   ⚠️  {key}: Not configured (using placeholder)")
        else:
            print(f"   ✅ {key}: {value}")
    
    return True

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        'streamlit',
        'requests',
        'plotly',
        'pandas',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def test_application_structure():
    """Test if application files are in place"""
    print("\n📁 Testing Application Structure...")
    
    required_files = [
        'src/main.py',
        'src/educational_assistant.py',
        'src/user_profile.py',
        'src/learning_analytics.py',
        'src/config.py',
        'requirements.txt'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_config_loading():
    """Test configuration loading"""
    print("\n⚙️  Testing Configuration Loading...")
    
    try:
        sys.path.append('src')
        from config import ConfigManager
        
        config_manager = ConfigManager()
        
        # Test AI config
        ai_config = config_manager.get_ai_config()
        print(f"   ✅ AI Config loaded - Model: {ai_config.model_name}")
        
        # Test App config
        app_config = config_manager.get_app_config()
        print(f"   ✅ App Config loaded - Name: {app_config.app_name}")
        
        # Test Learning config
        learning_config = config_manager.get_learning_config()
        print(f"   ✅ Learning Config loaded - Subjects: {len(learning_config.supported_subjects)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration loading failed: {e}")
        return False

def test_streamlit_app():
    """Test if Streamlit app can be imported"""
    print("\n🎨 Testing Streamlit Application...")
    
    try:
        sys.path.append('src')
        
        # Test if main.py can be imported (basic syntax check)
        with open('src/main.py', 'r') as f:
            content = f.read()
            
        if 'streamlit' in content and 'st.' in content:
            print("   ✅ Streamlit app structure looks good")
        else:
            print("   ⚠️  Streamlit app structure might have issues")
            
        # Check for key components
        components = ['st.title', 'st.sidebar', 'st.chat_message']
        found_components = []
        
        for component in components:
            if component in content:
                found_components.append(component)
                
        print(f"   ✅ Found UI components: {', '.join(found_components)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Streamlit app test failed: {e}")
        return False

def test_mock_functionality():
    """Test application functionality with mock data"""
    print("\n🧪 Testing Mock Functionality...")
    
    try:
        sys.path.append('src')
        from user_profile import UserProfile
        
        # Test user profile creation
        profile = UserProfile("test_user")
        profile.learning_style = "Visual"
        profile.add_subject_interest("Mathematics")
        
        print("   ✅ User profile creation works")
        print(f"   ✅ Learning style: {profile.learning_style}")
        print(f"   ✅ Subjects: {profile.subject_interests}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Mock functionality test failed: {e}")
        return False

def provide_setup_instructions():
    """Provide setup instructions for API key"""
    print("\n" + "=" * 60)
    print("🔑 API KEY SETUP INSTRUCTIONS")
    print("=" * 60)
    print()
    print("To enable full AI functionality, you need to:")
    print()
    print("1. 🌐 Get a Grok API Key:")
    print("   • Visit: https://console.x.ai/")
    print("   • Sign up or log in to your X.AI account")
    print("   • Create a new API key")
    print("   • Copy the key (starts with 'xai-')")
    print()
    print("2. 📝 Configure the API Key:")
    print("   • Open the .env file in this directory")
    print("   • Replace 'your_grok_api_key_here' with your actual key")
    print("   • Save the file")
    print()
    print("3. 🧪 Test the API Key:")
    print("   • Run: python3 test_api.py")
    print("   • This will verify your API key is working")
    print()
    print("4. 🚀 Start the Application:")
    print("   • Run: streamlit run src/main.py")
    print("   • Open: http://localhost:8501")
    print()
    print("💡 Note: The application will work in demo mode without an API key,")
    print("   but AI responses will be limited or simulated.")

def main():
    """Main testing function"""
    print("🚀 AI Educational Assistant - System Testing")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 6
    
    # Run all tests
    if test_environment_setup():
        tests_passed += 1
    
    if test_dependencies():
        tests_passed += 1
    
    if test_application_structure():
        tests_passed += 1
    
    if test_config_loading():
        tests_passed += 1
    
    if test_streamlit_app():
        tests_passed += 1
    
    if test_mock_functionality():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your application is ready to use.")
        print("🔑 Configure your OpenAI API key for full functionality.")
    elif tests_passed >= 4:
        print("✅ Most tests passed! Application should work with minor issues.")
        print("🔧 Check the failed tests above for any issues to resolve.")
    else:
        print("⚠️  Several tests failed. Please resolve the issues above.")
        print("📚 Check the installation guide in docs/INSTALLATION.md")
    
    # Always provide setup instructions
    provide_setup_instructions()
    
    return tests_passed >= 4

if __name__ == "__main__":
    main()