#!/usr/bin/env python3
"""
Generative AI Personalized Educational Assistant
Main application entry point
"""

import streamlit as st
import openai
from datetime import datetime
import json
import os
from typing import Dict, List, Any

from educational_assistant import EducationalAssistant
from user_profile import UserProfile
from learning_analytics import LearningAnalytics

def main():
    """Main application function"""
    st.set_page_config(
        page_title="AI Educational Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = EducationalAssistant()
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = UserProfile()
    if 'analytics' not in st.session_state:
        st.session_state.analytics = LearningAnalytics()
    
    # Sidebar for user profile and settings
    with st.sidebar:
        st.header("👤 User Profile")
        setup_user_profile()
        
        st.header("📊 Learning Analytics")
        display_analytics()
    
    # Main content area
    st.title("🎓 AI Personalized Educational Assistant")
    st.markdown("*Adaptive learning powered by generative AI*")
    
    # Chat interface
    display_chat_interface()
    
    # Learning recommendations
    display_recommendations()

def setup_user_profile():
    """Setup user profile in sidebar"""
    name = st.text_input("Name", value=st.session_state.user_profile.name)
    learning_style = st.selectbox(
        "Learning Style",
        ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"],
        index=0 if not st.session_state.user_profile.learning_style else 
        ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"].index(st.session_state.user_profile.learning_style)
    )
    subjects = st.multiselect(
        "Subjects of Interest",
        ["Mathematics", "Science", "History", "Literature", "Computer Science", "Languages"],
        default=st.session_state.user_profile.subjects
    )
    
    if st.button("Update Profile"):
        st.session_state.user_profile.update_profile(name, learning_style, subjects)
        st.success("Profile updated!")

def display_chat_interface():
    """Display the main chat interface"""
    st.header("💬 Ask Your AI Tutor")
    
    # Chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your studies..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.assistant.generate_response(
                    prompt, 
                    st.session_state.user_profile
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Update analytics
                st.session_state.analytics.log_interaction(prompt, response)

def display_recommendations():
    """Display personalized learning recommendations"""
    st.header("📚 Personalized Recommendations")
    
    if st.session_state.user_profile.subjects:
        recommendations = st.session_state.assistant.get_recommendations(
            st.session_state.user_profile
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📖 Study Materials")
            for rec in recommendations.get('materials', []):
                st.markdown(f"• {rec}")
        
        with col2:
            st.subheader("🎯 Learning Goals")
            for goal in recommendations.get('goals', []):
                st.markdown(f"• {goal}")

def display_analytics():
    """Display learning analytics in sidebar"""
    analytics = st.session_state.analytics.get_summary()
    
    st.metric("Questions Asked", analytics.get('total_questions', 0))
    st.metric("Study Sessions", analytics.get('sessions', 0))
    st.metric("Avg. Session Time", f"{analytics.get('avg_time', 0):.1f} min")
    
    if analytics.get('progress'):
        st.progress(analytics['progress'])
        st.caption(f"Learning Progress: {analytics['progress']*100:.0f}%")

if __name__ == "__main__":
    main()