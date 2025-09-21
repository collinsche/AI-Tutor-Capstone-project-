#!/usr/bin/env python3
"""
Educational Assistant Core Module
Handles AI interactions and personalized learning using Grok
"""

import logging
import requests
from config import get_ai_config, get_app_config
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

class EducationalAssistant:
    def __init__(self):
        self.config = get_ai_config()
        self.app_config = get_app_config()
        logging.basicConfig(level=self.app_config.log_level)
        self.api_key = self.config.api_key
        self.base_url = self.config.api_base_url or "https://openrouter.ai/api/v1"
        self.conversation_history = []
        self.learning_context = {}
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
        system_prompt = self._build_system_prompt(user_profile)
        if self.config.use_demo_mode:
            response = self._generate_demo_response(user_input, user_profile)
        else:
            try:
                logging.info(f"Generating response using Grok 4 Fast model: {self.config.model_name}")
                
                # Validate API key
                if not self.api_key or not self.api_key.startswith(('sk-', 'xai-', 'sk-or-')):
                    logging.warning("Invalid or missing Grok API key, falling back to demo mode")
                    response = self._generate_demo_response(user_input, user_profile)
                    response += "\n\n⚠️ Note: Please configure a valid Grok API key to use AI features."
                    return response
                
                messages = [
                    {"role": "system", "content": system_prompt},
                ] + [
                    item
                    for h in self.conversation_history
                    for item in (
                        {"role": "user", "content": h["user"]},
                        {"role": "assistant", "content": h["assistant"]}
                    )
                ] + [
                    {"role": "user", "content": user_input}
                ]
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "AI-Educational-Assistant/1.0"
                }
                
                payload = {
                    "model": self.config.model_name,
                    "messages": messages,
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens,
                    "top_p": getattr(self.config, 'top_p', 1.0),
                    "frequency_penalty": getattr(self.config, 'frequency_penalty', 0.0),
                    "presence_penalty": getattr(self.config, 'presence_penalty', 0.0),
                    "stream": False
                }
                
                logging.debug(f"Making request to Grok API: {self.base_url}/chat/completions")
                response_obj = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.config.timeout
                )
                
                # Enhanced error handling for different HTTP status codes
                if response_obj.status_code == 401:
                    logging.error("Grok API authentication failed - invalid API key")
                    response = self._generate_demo_response(user_input, user_profile)
                    response += "\n\n🔑 Authentication Error: Invalid Grok API key. Please check your API key configuration."
                elif response_obj.status_code == 403:
                    logging.error("Grok API access forbidden - insufficient permissions")
                    response = self._generate_demo_response(user_input, user_profile)
                    response += "\n\n🚫 Access Denied: Your Grok API key doesn't have sufficient permissions."
                elif response_obj.status_code == 429:
                    logging.error("Grok API rate limit exceeded")
                    response = self._generate_demo_response(user_input, user_profile)
                    response += "\n\n⏱️ Rate Limit: Too many requests to Grok API. Please try again later."
                elif response_obj.status_code == 500:
                    logging.error("Grok API server error")
                    response = self._generate_demo_response(user_input, user_profile)
                    response += "\n\n🔧 Server Error: Grok API is experiencing issues. Using demo mode."
                elif response_obj.status_code != 200:
                    logging.error(f"Grok API returned status code {response_obj.status_code}: {response_obj.text}")
                    response = self._generate_demo_response(user_input, user_profile)
                    response += f"\n\n❌ API Error ({response_obj.status_code}): Using demo mode."
                else:
                    response_data = response_obj.json()
                    
                    # Validate response structure
                    if "choices" not in response_data or not response_data["choices"]:
                        logging.error("Invalid response structure from Grok API")
                        response = self._generate_demo_response(user_input, user_profile)
                        response += "\n\n⚠️ Invalid API response structure. Using demo mode."
                    else:
                        response = response_data["choices"][0]["message"]["content"]
                        logging.info(f"Successfully generated response using Grok 4 Fast model")
                        
                        # Log usage information if available
                        if "usage" in response_data:
                            usage = response_data["usage"]
                            logging.info(f"Token usage - Prompt: {usage.get('prompt_tokens', 0)}, "
                                       f"Completion: {usage.get('completion_tokens', 0)}, "
                                       f"Total: {usage.get('total_tokens', 0)}")
                
            except requests.exceptions.Timeout:
                logging.error(f"Grok API request timeout after {self.config.timeout} seconds")
                response = self._generate_demo_response(user_input, user_profile)
                response += "\n\n⏰ Timeout: Grok API request took too long. Using demo mode."
            except requests.exceptions.ConnectionError:
                logging.error("Failed to connect to Grok API")
                response = self._generate_demo_response(user_input, user_profile)
                response += "\n\n🌐 Connection Error: Unable to reach Grok API. Check your internet connection."
            except requests.exceptions.RequestException as e:
                logging.error(f"Grok API request error: {str(e)}")
                response = self._generate_demo_response(user_input, user_profile)
                response += "\n\n🔗 Network Error: Problem communicating with Grok API. Using demo mode."
            except json.JSONDecodeError:
                logging.error("Failed to parse Grok API response as JSON")
                response = self._generate_demo_response(user_input, user_profile)
                response += "\n\n📄 Parse Error: Invalid response from Grok API. Using demo mode."
            except KeyError as e:
                logging.error(f"Missing expected field in Grok API response: {str(e)}")
                response = self._generate_demo_response(user_input, user_profile)
                response += "\n\n🔍 Response Error: Unexpected API response format. Using demo mode."
            except Exception as e:
                logging.error(f"Unexpected error generating response: {str(e)}", exc_info=True)
                response = self._generate_demo_response(user_input, user_profile)
                response += "\n\n❓ Unexpected Error: An unknown error occurred. Using demo mode."
        
        # Store conversation history
        self.conversation_history.append({
            "user": user_input,
            "assistant": response,
            "timestamp": datetime.now().isoformat(),
            "model": self.config.model_name,
            "mode": "demo" if self.config.use_demo_mode else "api"
        })
        
        return response

    def _build_system_prompt(self, user_profile) -> str:
        """Build system prompt based on user profile"""
        learning_style = user_profile.get('learning_style', 'Visual')
        subjects = ", ".join(user_profile.get('subjects', [])) if user_profile.get('subjects') else "general topics"
        
        strategies = self.learning_strategies.get(learning_style, self.learning_strategies["Visual"])
        
        prompt = f"""
        You are an AI educational assistant specialized in personalized learning.
        
        Student Profile:
        - Name: {user_profile.get('name', 'Student')}
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
        """Generate demo response (replace with Grok API in production)"""
        learning_style = user_profile.get('learning_style', 'Visual')
        name = user_profile.get('name', 'there')
        
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
        learning_style = user_profile.get('learning_style', 'Visual')
        subjects = user_profile.get('subjects', ['General Studies'])
        
        # Map full learning style descriptions to simple keys
        style_mapping = {
            "Visual (diagrams, charts, images)": "Visual",
            "Auditory (listening, discussions)": "Auditory", 
            "Kinesthetic (hands-on, practice)": "Kinesthetic",
            "Reading/Writing (text-based)": "Reading/Writing"
        }
        
        # Get the mapped style or use the original if it's already mapped
        mapped_style = style_mapping.get(learning_style, learning_style)
        
        # Fallback to Visual if the style is not found
        if mapped_style not in self.learning_strategies:
            mapped_style = "Visual"
            
        strategies = self.learning_strategies[mapped_style]
        
        materials = []
        goals = []
        
        for subject in subjects[:3]:  # Limit to 3 subjects
            if mapped_style == "Visual":
                materials.append(f"Interactive {subject} diagrams and infographics")
                materials.append(f"Video tutorials for {subject} concepts")
            elif mapped_style == "Auditory":
                materials.append(f"{subject} podcasts and audio lectures")
                materials.append(f"Discussion groups for {subject}")
            elif mapped_style == "Kinesthetic":
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