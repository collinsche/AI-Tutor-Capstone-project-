#!/usr/bin/env python3
"""
Test Suite for AI Educational Assistant
"""

import pytest
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from educational_assistant import EducationalAssistant
from user_profile import UserProfile
from learning_analytics import LearningAnalytics
from utils import sanitize_input, extract_keywords, calculate_similarity
from config import ConfigManager

class TestEducationalAssistant:
    """Test cases for EducationalAssistant class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.assistant = EducationalAssistant()
        self.user_profile = UserProfile()
        self.user_profile.update_profile(
            name="Test User",
            learning_style="Visual",
            subjects=["Mathematics", "Science"]
        )
    
    def test_initialization(self):
        """Test assistant initialization"""
        assert self.assistant is not None
        assert hasattr(self.assistant, 'conversation_history')
        assert hasattr(self.assistant, 'learning_strategies')
    
    def test_generate_response(self):
        """Test response generation"""
        response = self.assistant.generate_response(
            "What is algebra?", 
            self.user_profile
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "Test User" in response or "there" in response
    
    def test_math_response(self):
        """Test math-specific response"""
        response = self.assistant._generate_math_response(
            "Help me with algebra",
            "Visual",
            "Test User"
        )
        
        assert "Test User" in response
        assert "visual" in response.lower()
    
    def test_get_recommendations(self):
        """Test recommendation generation"""
        recommendations = self.assistant.get_recommendations(self.user_profile)
        
        assert isinstance(recommendations, dict)
        assert "materials" in recommendations
        assert "goals" in recommendations
        assert len(recommendations["materials"]) > 0
        assert len(recommendations["goals"]) > 0
    
    def test_conversation_history(self):
        """Test conversation history tracking"""
        initial_count = len(self.assistant.get_conversation_history())
        
        self.assistant.generate_response("Test question", self.user_profile)
        
        assert len(self.assistant.get_conversation_history()) == initial_count + 1
        
        # Test clear history
        self.assistant.clear_history()
        assert len(self.assistant.get_conversation_history()) == 0

class TestUserProfile:
    """Test cases for UserProfile class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.profile = UserProfile("test_profile.json")
    
    def teardown_method(self):
        """Clean up test files"""
        if os.path.exists("test_profile.json"):
            os.remove("test_profile.json")
    
    def test_initialization(self):
        """Test profile initialization"""
        assert self.profile.name == ""
        assert self.profile.learning_style == "Visual"
        assert self.profile.subjects == []
    
    def test_update_profile(self):
        """Test profile update"""
        self.profile.update_profile(
            name="John Doe",
            learning_style="Auditory",
            subjects=["History", "Literature"]
        )
        
        assert self.profile.name == "John Doe"
        assert self.profile.learning_style == "Auditory"
        assert "History" in self.profile.subjects
        assert "Literature" in self.profile.subjects
    
    def test_learning_session(self):
        """Test learning session tracking"""
        session_data = {
            "duration": 30,
            "topics": ["algebra", "geometry"],
            "questions": 5,
            "difficulty": "medium",
            "satisfaction": 4
        }
        
        initial_count = len(self.profile.learning_history)
        self.profile.add_learning_session(session_data)
        
        assert len(self.profile.learning_history) == initial_count + 1
        assert self.profile.learning_history[-1]["duration"] == 30
    
    def test_progress_summary(self):
        """Test progress summary generation"""
        # Add some test sessions
        for i in range(3):
            self.profile.add_learning_session({
                "duration": 20 + i * 10,
                "topics": [f"topic_{i}"],
                "satisfaction": 3 + i
            })
        
        summary = self.profile.get_progress_summary()
        
        assert summary["total_sessions"] == 3
        assert summary["total_time"] == 90  # 20 + 30 + 40
        assert summary["average_satisfaction"] > 0

class TestLearningAnalytics:
    """Test cases for LearningAnalytics class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analytics = LearningAnalytics("test_analytics.json")
    
    def teardown_method(self):
        """Clean up test files"""
        if os.path.exists("test_analytics.json"):
            os.remove("test_analytics.json")
    
    def test_initialization(self):
        """Test analytics initialization"""
        assert self.analytics is not None
        assert hasattr(self.analytics, 'interactions')
        assert hasattr(self.analytics, 'sessions')
    
    def test_session_management(self):
        """Test session start and end"""
        self.analytics.start_session("test_user")
        assert self.analytics.current_session is not None
        assert self.analytics.current_session["user_id"] == "test_user"
        
        self.analytics.end_session()
        assert self.analytics.current_session is None
        assert len(self.analytics.sessions) == 1
    
    def test_log_interaction(self):
        """Test interaction logging"""
        initial_count = len(self.analytics.interactions)
        
        self.analytics.log_interaction(
            "What is calculus?",
            "Calculus is a branch of mathematics...",
            ["mathematics"]
        )
        
        assert len(self.analytics.interactions) == initial_count + 1
        interaction = self.analytics.interactions[-1]
        assert interaction["user_input"] == "What is calculus?"
        assert "mathematics" in interaction["topics"]
    
    def test_topic_extraction(self):
        """Test topic extraction from text"""
        topics = self.analytics._extract_topics("I need help with algebra and geometry")
        assert "mathematics" in topics
        
        topics = self.analytics._extract_topics("Tell me about World War II")
        assert "history" in topics
    
    def test_interaction_classification(self):
        """Test interaction type classification"""
        question_type = self.analytics._classify_interaction("What is photosynthesis?")
        assert question_type == "question"
        
        help_type = self.analytics._classify_interaction("Help me understand this concept")
        assert help_type == "help_request"
        
        practice_type = self.analytics._classify_interaction("I want to practice problems")
        assert practice_type == "practice_request"
    
    def test_get_summary(self):
        """Test analytics summary"""
        # Add some test data
        self.analytics.start_session()
        self.analytics.log_interaction("Test question", "Test response")
        self.analytics.end_session()
        
        summary = self.analytics.get_summary()
        
        assert "total_questions" in summary
        assert "sessions" in summary
        assert summary["sessions"] >= 1

class TestUtils:
    """Test cases for utility functions"""
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        clean_input = sanitize_input("Hello world!")
        assert clean_input == "Hello world!"
        
        malicious_input = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in malicious_input
        assert "alert" in malicious_input  # Content preserved, tags removed
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        text = "Machine learning is a subset of artificial intelligence that focuses on algorithms"
        keywords = extract_keywords(text, max_keywords=5)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        assert "machine" in keywords or "learning" in keywords
    
    def test_calculate_similarity(self):
        """Test text similarity calculation"""
        text1 = "machine learning algorithms"
        text2 = "algorithms for machine learning"
        
        similarity = calculate_similarity(text1, text2)
        assert 0 <= similarity <= 1
        assert similarity > 0.5  # Should be fairly similar
        
        # Test with completely different texts
        similarity_low = calculate_similarity("cats and dogs", "space exploration")
        assert similarity_low < 0.5

class TestConfig:
    """Test cases for configuration management"""
    
    def test_config_initialization(self):
        """Test configuration initialization"""
        config = ConfigManager()
        
        assert config.ai_config is not None
        assert config.app_config is not None
        assert config.learning_config is not None
        assert config.ui_config is not None
    
    def test_config_validation(self):
        """Test configuration validation"""
        config = ConfigManager()
        issues = config.validate_config()
        
        assert "errors" in issues
        assert "warnings" in issues
        assert isinstance(issues["errors"], list)
        assert isinstance(issues["warnings"], list)
    
    def test_config_update(self):
        """Test configuration updates"""
        config = ConfigManager()
        original_temp = config.ai_config.temperature
        
        config.update_config("ai", temperature=0.5)
        assert config.ai_config.temperature == 0.5
        assert config.ai_config.temperature != original_temp

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])