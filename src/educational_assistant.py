#!/usr/bin/env python3
"""
Educational Assistant Core Module
Handles AI interactions and personalized learning
"""

import openai
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

class EducationalAssistant:
    """Core AI Educational Assistant class"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the educational assistant"""
        self.api_key = api_key or "your-openai-api-key-here"
        # Note: In production, use environment variables for API keys
        # openai.api_key = self.api_key
        
        self.conversation_history = []
        self.learning_context = {}
        
        # Predefined learning strategies for different styles
        self.learning_strategies = {
            "Visual": {
                "techniques": ["diagrams", "charts", "mind maps", "infographics"],
                "content_format": "visual_heavy",
                "examples": "graphical"
            },
            "Auditory": {
                "techniques": ["discussions", "lectures", "audio content", "verbal explanations"],
                "content_format": "conversational",
                "examples": "spoken"
            },
            "Kinesthetic": {
                "techniques": ["hands-on activities", "experiments", "simulations", "practice problems"],
                "content_format": "interactive",
                "examples": "practical"
            },
            "Reading/Writing": {
                "techniques": ["note-taking", "written summaries", "text analysis", "essays"],
                "content_format": "text_heavy",
                "examples": "written"
            }
        }
    
    def generate_response(self, user_input: str, user_profile) -> str:
        """Generate personalized AI response based on user profile"""
        try:
            # Build context-aware prompt
            system_prompt = self._build_system_prompt(user_profile)
            
            # For demo purposes, we'll use a rule-based approach
            # In production, this would use OpenAI's API
            response = self._generate_demo_response(user_input, user_profile)
            
            # Update conversation history
            self.conversation_history.append({
                "user": user_input,
                "assistant": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def _build_system_prompt(self, user_profile) -> str:
        """Build system prompt based on user profile"""
        learning_style = user_profile.learning_style or "Visual"
        subjects = ", ".join(user_profile.subjects) if user_profile.subjects else "general topics"
        
        strategies = self.learning_strategies.get(learning_style, self.learning_strategies["Visual"])
        
        prompt = f"""
        You are an AI educational assistant specialized in personalized learning.
        
        Student Profile:
        - Name: {user_profile.name or 'Student'}
        - Learning Style: {learning_style}
        - Subjects: {subjects}
        
        Teaching Approach:
        - Use {learning_style.lower()} learning techniques
        - Focus on: {', '.join(strategies['techniques'])}
        - Content format: {strategies['content_format']}
        - Provide {strategies['examples']} examples
        
        Always:
        1. Adapt explanations to the student's learning style
        2. Provide relevant examples and analogies
        3. Encourage active learning
        4. Break down complex topics into manageable parts
        5. Ask follow-up questions to check understanding
        """
        
        return prompt
    
    def _generate_demo_response(self, user_input: str, user_profile) -> str:
        """Generate demo response (replace with OpenAI API in production)"""
        learning_style = user_profile.learning_style or "Visual"
        name = user_profile.name or "there"
        
        # Simple keyword-based responses for demo
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['math', 'mathematics', 'algebra', 'calculus']):
            return self._generate_math_response(user_input, learning_style, name)
        elif any(word in user_input_lower for word in ['science', 'physics', 'chemistry', 'biology']):
            return self._generate_science_response(user_input, learning_style, name)
        elif any(word in user_input_lower for word in ['history', 'historical']):
            return self._generate_history_response(user_input, learning_style, name)
        elif any(word in user_input_lower for word in ['help', 'study', 'learn']):
            return self._generate_study_help_response(learning_style, name)
        else:
            return self._generate_general_response(user_input, learning_style, name)
    
    def _generate_math_response(self, question: str, learning_style: str, name: str) -> str:
        """Generate math-specific response based on learning style"""
        responses = {
            "Visual": f"Hi {name}! Let me help you with math using visual approaches. I'd recommend creating diagrams or graphs to visualize the problem. Would you like me to suggest some visual techniques for the specific math topic you're working on?",
            "Auditory": f"Hello {name}! For math, I suggest talking through problems step-by-step. Try explaining the problem out loud or discussing it with others. What specific math concept would you like to explore through discussion?",
            "Kinesthetic": f"Hey {name}! Math becomes clearer with hands-on practice. Let's work through some practice problems together. What math topic are you struggling with? I can guide you through interactive problem-solving.",
            "Reading/Writing": f"Hi {name}! Taking detailed notes and writing out each step helps with math. I recommend creating written summaries of key formulas and concepts. What math area would you like to focus on?"
        }
        return responses.get(learning_style, responses["Visual"])
    
    def _generate_science_response(self, question: str, learning_style: str, name: str) -> str:
        """Generate science-specific response based on learning style"""
        responses = {
            "Visual": f"Great question, {name}! Science concepts are perfect for visual learning. I suggest using diagrams, flowcharts, and concept maps. What specific science topic interests you?",
            "Auditory": f"Excellent, {name}! Science discussions and explanations work well for auditory learners. Let's talk through the concepts. Which science subject would you like to explore?",
            "Kinesthetic": f"Perfect, {name}! Science is all about experimentation and hands-on learning. I can suggest virtual labs or practical activities. What science area are you curious about?",
            "Reading/Writing": f"Good choice, {name}! Writing scientific explanations and taking detailed notes helps solidify understanding. What science topic would you like to dive into?"
        }
        return responses.get(learning_style, responses["Visual"])
    
    def _generate_history_response(self, question: str, learning_style: str, name: str) -> str:
        """Generate history-specific response based on learning style"""
        responses = {
            "Visual": f"History comes alive with visuals, {name}! Try timelines, maps, and historical images. What historical period interests you most?",
            "Auditory": f"History is full of great stories, {name}! I recommend historical podcasts and discussions. Which historical era would you like to explore?",
            "Kinesthetic": f"History through experience works great, {name}! Virtual museum tours and historical simulations can help. What historical topic are you studying?",
            "Reading/Writing": f"Historical analysis through writing is powerful, {name}! Try creating summaries and essays. What historical period would you like to focus on?"
        }
        return responses.get(learning_style, responses["Visual"])
    
    def _generate_study_help_response(self, learning_style: str, name: str) -> str:
        """Generate general study help response"""
        strategies = self.learning_strategies[learning_style]
        techniques = ", ".join(strategies['techniques'][:3])
        
        return f"I'm here to help you study effectively, {name}! Based on your {learning_style.lower()} learning style, I recommend focusing on {techniques}. What subject would you like to work on today?"
    
    def _generate_general_response(self, question: str, learning_style: str, name: str) -> str:
        """Generate general response"""
        return f"That's an interesting question, {name}! I'll adapt my explanation to your {learning_style.lower()} learning style. Could you provide more details about what you'd like to learn?"
    
    def get_recommendations(self, user_profile) -> Dict[str, List[str]]:
        """Get personalized learning recommendations"""
        learning_style = user_profile.learning_style or "Visual"
        subjects = user_profile.subjects or ["General Studies"]
        
        strategies = self.learning_strategies[learning_style]
        
        materials = []
        goals = []
        
        for subject in subjects[:3]:  # Limit to 3 subjects
            if learning_style == "Visual":
                materials.append(f"Interactive {subject} diagrams and infographics")
                materials.append(f"Video tutorials for {subject} concepts")
            elif learning_style == "Auditory":
                materials.append(f"{subject} podcasts and audio lectures")
                materials.append(f"Discussion groups for {subject}")
            elif learning_style == "Kinesthetic":
                materials.append(f"Hands-on {subject} experiments and simulations")
                materials.append(f"Interactive {subject} practice problems")
            else:  # Reading/Writing
                materials.append(f"Comprehensive {subject} textbooks and articles")
                materials.append(f"{subject} writing exercises and note templates")
            
            goals.append(f"Master key {subject} concepts this week")
            goals.append(f"Complete {subject} practice exercises daily")
        
        return {
            "materials": materials[:6],  # Limit to 6 items
            "goals": goals[:6]
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []