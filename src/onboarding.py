#!/usr/bin/env python3
"""
AI-Driven User Onboarding and Profiling System
Implements interactive quiz and chat interface for comprehensive user assessment
"""

import streamlit as st
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from educational_assistant import EducationalAssistant

class OnboardingSystem:
    """AI-driven onboarding system for creating comprehensive user profiles"""
    
    def __init__(self):
        self.questions = self._load_onboarding_questions()
        self.assistant = EducationalAssistant()
        
    def _load_onboarding_questions(self) -> List[Dict[str, Any]]:
        """Load structured onboarding questions"""
        return [
            {
                "id": "learning_style",
                "type": "multiple_choice",
                "question": "How do you prefer to learn new concepts?",
                "options": [
                    "Visual (diagrams, charts, images)",
                    "Auditory (listening, discussions)",
                    "Kinesthetic (hands-on, practice)",
                    "Reading/Writing (text-based)"
                ],
                "category": "learning_preference"
            },
            {
                "id": "experience_level",
                "type": "multiple_choice", 
                "question": "What's your current experience level?",
                "options": [
                    "Complete Beginner",
                    "Some Basic Knowledge",
                    "Intermediate",
                    "Advanced"
                ],
                "category": "skill_level"
            },
            {
                "id": "learning_goals",
                "type": "multiple_select",
                "question": "What are your primary learning goals?",
                "options": [
                    "Career advancement",
                    "Personal interest",
                    "Academic requirements",
                    "Skill development",
                    "Problem solving"
                ],
                "category": "motivation"
            },
            {
                "id": "subjects",
                "type": "multiple_select",
                "question": "Which subjects interest you most?",
                "options": [
                    "Mathematics", "Science", "Programming", 
                    "Languages", "History", "Arts", "Business"
                ],
                "category": "interests"
            },
            {
                "id": "time_availability",
                "type": "multiple_choice",
                "question": "How much time can you dedicate to learning daily?",
                "options": [
                    "15-30 minutes",
                    "30-60 minutes", 
                    "1-2 hours",
                    "2+ hours"
                ],
                "category": "schedule"
            }
        ]
    
    def run_interactive_assessment(self) -> Dict[str, Any]:
        """Run the interactive onboarding assessment"""
        st.title("🎯 Personalized Learning Setup")
        st.markdown("Let's create your personalized learning profile!")
        
        # Initialize session state
        if 'onboarding_responses' not in st.session_state:
            st.session_state.onboarding_responses = {}
        if 'onboarding_step' not in st.session_state:
            st.session_state.onboarding_step = 0
        if 'onboarding_complete' not in st.session_state:
            st.session_state.onboarding_complete = False
            
        # Display current question or completion
        if st.session_state.onboarding_step < len(self.questions):
            # Progress bar for active questions
            progress = st.session_state.onboarding_step / len(self.questions)
            st.progress(progress)
            st.write(f"Step {st.session_state.onboarding_step + 1} of {len(self.questions)}")
            
            self._display_question(self.questions[st.session_state.onboarding_step])
        else:
            # Show completion progress
            st.progress(1.0)
            st.write(f"Setup Complete!")
            self._complete_assessment()
            
        return st.session_state.get('user_profile', {})
    
    def _display_question(self, question: Dict[str, Any]):
        """Display a single question"""
        st.subheader(question["question"])
        
        if question["type"] == "multiple_choice":
            response = st.radio(
                "Select one:",
                question["options"],
                key=f"q_{question['id']}"
            )
            
        elif question["type"] == "multiple_select":
            response = st.multiselect(
                "Select all that apply:",
                question["options"],
                key=f"q_{question['id']}"
            )
            
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.onboarding_step > 0:
                if st.button("← Previous"):
                    st.session_state.onboarding_step -= 1
                    st.rerun()
        
        with col3:
            if st.button("Next →"):
                # Save response
                st.session_state.onboarding_responses[question["id"]] = response
                st.session_state.onboarding_step += 1
                st.rerun()
    
    def _complete_assessment(self):
        """Complete the assessment and generate profile"""
        st.success("🎉 Assessment Complete!")
        st.markdown("Generating your personalized learning profile...")
        
        # Generate profile analysis
        analysis = self._generate_profile_analysis()
        
        # Display profile summary
        st.subheader("Your Learning Profile")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Learning Style", analysis.get("learning_style", "Visual"))
            st.metric("Experience Level", analysis.get("experience_level", "Beginner"))
            
        with col2:
            st.metric("Daily Study Time", analysis.get("time_availability", "30-60 minutes"))
            st.metric("Primary Goals", len(analysis.get("learning_goals", [])))
        
        # Save profile
        self._save_profile(analysis)
        
        if st.button("Start Learning Journey! 🚀"):
            st.session_state.onboarding_complete = True
            st.session_state.user_profile_complete = True  # Set the flag that app_router checks
            st.rerun()

    def _generate_profile_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive profile analysis"""
        responses = st.session_state.onboarding_responses
        
        return {
            "name": st.text_input("What's your name?", key="user_name") or "Learner",
            "learning_style": responses.get("learning_style", "Visual"),
            "experience_level": responses.get("experience_level", "Beginner"),
            "learning_goals": responses.get("learning_goals", []),
            "subjects": responses.get("subjects", []),
            "time_availability": responses.get("time_availability", "30-60 minutes"),
            "created_at": datetime.now().isoformat(),
            "preferences": {
                "difficulty_preference": "adaptive",
                "content_format": "mixed",
                "feedback_style": "encouraging"
            }
        }

    def _save_profile(self, analysis: Dict[str, Any]):
        """Save the generated profile"""
        st.session_state.user_profile = analysis
        
        # Also save to file for persistence
        try:
            with open("user_profile.json", "w") as f:
                json.dump(analysis, f, indent=2)
        except Exception as e:
            st.warning(f"Could not save profile to file: {e}")

    def is_onboarding_complete(self) -> bool:
        """Check if onboarding is complete"""
        # Check if user profile exists in session state
        if hasattr(st.session_state, 'user_profile') and st.session_state.user_profile:
            return True
        
        # Check if profile file exists
        try:
            with open("user_profile.json", "r") as f:
                profile = json.load(f)
                if profile and 'preferences' in profile:
                    st.session_state.user_profile = profile
                    return True
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        return False

    def reset_onboarding(self):
        """Reset the onboarding process"""
        # Clear session state
        if hasattr(st.session_state, 'user_profile'):
            del st.session_state.user_profile
        if hasattr(st.session_state, 'onboarding_responses'):
            del st.session_state.onboarding_responses
        
        # Remove profile file
        try:
            import os
            if os.path.exists("user_profile.json"):
                os.remove("user_profile.json")
        except Exception:
            pass


def run_onboarding_chat():
    """Run the onboarding chat interface"""
    st.title("🎯 Welcome to Your AI Educational Assistant!")
    st.markdown("Let's get to know you better to personalize your learning experience.")
    
    # Initialize onboarding system
    onboarding = OnboardingSystem()
    
    # Run the interactive assessment
    profile = onboarding.run_interactive_assessment()
    
    return profile


class OnboardingInterface:
    """Streamlit interface for onboarding"""
    
    def __init__(self, onboarding_system: OnboardingSystem):
        self.onboarding_system = onboarding_system
    
    def render_onboarding(self):
        """Render the onboarding interface"""
        profile = self.onboarding_system.run_interactive_assessment()
        return profile
    
    def is_complete(self) -> bool:
        """Check if onboarding is complete"""
        return self.onboarding_system.is_onboarding_complete()
    
    def reset(self):
        """Reset the onboarding process"""
        self.onboarding_system.reset_onboarding()