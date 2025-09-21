#!/usr/bin/env python3
"""
Test Runner Module
Comprehensive testing suite for the AI Educational Assistant
"""

import sys
import json
from datetime import datetime

# Import all modules to test
from user_profile import UserProfile
from educational_assistant import EducationalAssistant
from learning_analytics import LearningAnalytics


def test_imports():
    """Test that all modules can be imported successfully"""
    print("🔍 Testing module imports...")
    
    modules_to_test = [
        ('user_profile', 'UserProfile'),
        ('educational_assistant', 'EducationalAssistant'),
        ('learning_analytics', 'LearningAnalytics'),
        ('onboarding', 'OnboardingInterface'),
        ('learning_paths', 'LearningPathGenerator'),
        ('enhanced_chat', 'EnhancedChatInterface'),
        ('adaptive_quiz', 'AdaptiveQuizInterface'),
        ('content_generator', 'ContentGenerator'),
        ('dashboard', 'DashboardManager'),
        ('app_router', 'AppRouter'),
        ('main', None)
    ]
    
    results = {}
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name)
            if class_name:
                getattr(module, class_name)
            results[f"{module_name}_import"] = "✅ SUCCESS"
            print(f"  ✅ {module_name}")
        except Exception as e:
            results[f"{module_name}_import"] = f"❌ FAILED: {str(e)}"
            print(f"  ❌ {module_name}: {str(e)}")
    
    return results


def test_core_components():
    """Test core component initialization"""
    print("\n🧪 Testing core component initialization...")
    
    results = {}
    
    # Test UserProfile
    try:
        profile = UserProfile()
        results['UserProfile_init'] = "✅ SUCCESS"
        print("  ✅ UserProfile initialization")
    except Exception as e:
        results['UserProfile_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ UserProfile: {str(e)}")

    # Test EducationalAssistant
    try:
        assistant = EducationalAssistant()
        results['EducationalAssistant_init'] = "✅ SUCCESS"
        print("  ✅ EducationalAssistant initialization")
    except Exception as e:
        results['EducationalAssistant_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ EducationalAssistant: {str(e)}")

    # Test LearningAnalytics
    try:
        analytics = LearningAnalytics()
        results['LearningAnalytics_init'] = "✅ SUCCESS"
        print("  ✅ LearningAnalytics initialization")
    except Exception as e:
        results['LearningAnalytics_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ LearningAnalytics: {str(e)}")
    
    return results


def test_advanced_components():
    """Test advanced component initialization"""
    print("\n🚀 Testing advanced component initialization...")
    
    results = {}
    
    # Test OnboardingInterface
    try:
        from onboarding import OnboardingInterface, OnboardingSystem
        onboarding = OnboardingInterface(OnboardingSystem())
        results['OnboardingInterface_init'] = "✅ SUCCESS"
        print("  ✅ OnboardingInterface initialization")
    except Exception as e:
        results['OnboardingInterface_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ OnboardingInterface: {str(e)}")

    # Test LearningPathGenerator
    try:
        from learning_paths import LearningPathGenerator
        path_gen = LearningPathGenerator()
        results['LearningPathGenerator_init'] = "✅ SUCCESS"
        print("  ✅ LearningPathGenerator initialization")
    except Exception as e:
        results['LearningPathGenerator_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ LearningPathGenerator: {str(e)}")

    # Test EnhancedChatInterface
    try:
        from enhanced_chat import EnhancedChatInterface
        assistant = EducationalAssistant()
        chat = EnhancedChatInterface(assistant)
        results['EnhancedChatInterface_init'] = "✅ SUCCESS"
        print("  ✅ EnhancedChatInterface initialization")
    except Exception as e:
        results['EnhancedChatInterface_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ EnhancedChatInterface: {str(e)}")

    # Test AdaptiveQuizInterface
    try:
        from adaptive_quiz import AdaptiveQuizInterface
        assistant = EducationalAssistant()
        quiz = AdaptiveQuizInterface(assistant)
        results['AdaptiveQuizInterface_init'] = "✅ SUCCESS"
        print("  ✅ AdaptiveQuizInterface initialization")
    except Exception as e:
        results['AdaptiveQuizInterface_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ AdaptiveQuizInterface: {str(e)}")

    # Test ContentGenerator
    try:
        from content_generator import ContentGenerator
        assistant = EducationalAssistant()
        content_gen = ContentGenerator(assistant)
        results['ContentGenerator_init'] = "✅ SUCCESS"
        print("  ✅ ContentGenerator initialization")
    except Exception as e:
        results['ContentGenerator_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ ContentGenerator: {str(e)}")

    # Test DashboardManager
    try:
        from dashboard import DashboardManager
        analytics = LearningAnalytics()
        dashboard = DashboardManager(analytics)
        results['DashboardManager_init'] = "✅ SUCCESS"
        print("  ✅ DashboardManager initialization")
    except Exception as e:
        results['DashboardManager_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ DashboardManager: {str(e)}")
    
    return results


def test_app_router():
    """Test AppRouter initialization"""
    print("\n🌐 Testing AppRouter initialization...")
    
    results = {}
    
    try:
        from app_router import AppRouter
        router = AppRouter()
        results['AppRouter_init'] = "✅ SUCCESS"
        print("  ✅ AppRouter initialization successful")
    except Exception as e:
        results['AppRouter_init'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ AppRouter initialization failed: {str(e)}")
    
    return results


def test_functionality():
    """Test basic functionality of key components"""
    print("\n⚙️ Testing basic functionality...")
    
    results = {}
    
    try:
        # Test UserProfile functionality
        profile = UserProfile()
        profile.update_profile("Test User", "Visual", ["Python", "Math"])
        profile_dict = profile.to_dict()
        
        if isinstance(profile_dict, dict) and 'name' in profile_dict:
            results['UserProfile_functionality'] = "✅ SUCCESS"
            print("  ✅ UserProfile update/export functionality")
        else:
            results['UserProfile_functionality'] = "❌ FAILED: Invalid profile format"
            print("  ❌ UserProfile functionality failed")
            
    except Exception as e:
        results['UserProfile_functionality'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ UserProfile functionality: {str(e)}")
    
    try:
        # Test LearningAnalytics functionality
        analytics = LearningAnalytics()
        analytics.start_session("test_user")
        analytics.log_interaction("test_user", "question", "Test question", {"test": True})
        summary = analytics.get_summary()
        
        if isinstance(summary, dict) and 'total_sessions' in summary:
            results['LearningAnalytics_functionality'] = "✅ SUCCESS"
            print("  ✅ LearningAnalytics session/interaction functionality")
        else:
            results['LearningAnalytics_functionality'] = "❌ FAILED: Invalid summary format"
            print("  ❌ LearningAnalytics functionality failed")
            
    except Exception as e:
        results['LearningAnalytics_functionality'] = f"❌ FAILED: {str(e)}"
        print(f"  ❌ LearningAnalytics functionality: {str(e)}")
    
    return results


def generate_report(all_results):
    """Generate comprehensive test report"""
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST REPORT")
    print("=" * 60)
    
    # Group results by category
    categories = {
        'imports': {},
        'core_components': {},
        'advanced_components': {},
        'app_router': {},
        'functionality': {}
    }
    
    for test_name, result in all_results.items():
        if 'import' in test_name:
            categories['imports'][test_name] = result
        elif test_name in ['UserProfile_init', 'EducationalAssistant_init', 'LearningAnalytics_init']:
            categories['core_components'][test_name] = result
        elif 'init' in test_name and test_name != 'AppRouter_init':
            categories['advanced_components'][test_name] = result
        elif 'AppRouter' in test_name:
            categories['app_router'][test_name] = result
        elif 'functionality' in test_name:
            categories['functionality'][test_name] = result
    
    # Print categorized results
    for category, tests in categories.items():
        if tests:
            print(f"\n📋 {category.upper().replace('_', ' ')}:")
            print("-" * 40)
            for test_name, result in tests.items():
                print(f"  {test_name}: {result}")
    
    # Calculate summary statistics
    total_tests = len(all_results)
    passed_tests = sum(1 for result in all_results.values() if "✅ SUCCESS" in result)
    
    print("\n" + "=" * 60)
    print(f"📈 SUMMARY: {passed_tests}/{total_tests} tests passed")
    print(f"✅ Success Rate: {(passed_tests / total_tests) * 100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Application is ready for demonstration.")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    print("=" * 60)
    
    return {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'success_rate': (passed_tests / total_tests) * 100,
        'results': all_results,
        'timestamp': datetime.now().isoformat()
    }


def main():
    """Main test runner function"""
    print("🚀 AI Educational Assistant - Comprehensive Test Suite")
    print("=" * 60)
    
    # Run all tests
    all_results = {}
    
    all_results.update(test_imports())
    all_results.update(test_core_components())
    all_results.update(test_advanced_components())
    all_results.update(test_app_router())
    all_results.update(test_functionality())
    
    # Generate comprehensive report
    report = generate_report(all_results)
    
    # Save results to file
    try:
        with open('test_results.json', 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Test results saved to test_results.json")
    except Exception as e:
        print(f"\n⚠️  Could not save test results: {str(e)}")


if __name__ == "__main__":
    main()