#!/usr/bin/env python3
"""
Enhanced Chat Interface for AI Educational Assistant
Real-time queries with Grok AI integration, code snippets, and advanced features
"""

import streamlit as st
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time
import os
from educational_assistant import EducationalAssistant

@dataclass
class ChatMessage:
    """Represents a chat message"""
    id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    message_type: str  # "text", "code", "explanation", "quiz"
    metadata: Dict[str, Any]

@dataclass
class CodeSnippet:
    """Represents a code snippet with syntax highlighting"""
    language: str
    code: str
    explanation: str
    is_runnable: bool

class EnhancedChatInterface:
    """Enhanced chat interface with AI integration"""
    
    def __init__(self, educational_assistant: EducationalAssistant):
        self.assistant = educational_assistant
        self.initialize_session_state()
        
    def initialize_session_state(self):
        """Initialize chat-related session state"""
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'typing_indicator' not in st.session_state:
            st.session_state.typing_indicator = False
        if 'current_topic' not in st.session_state:
            st.session_state.current_topic = None
        if 'code_execution_enabled' not in st.session_state:
            st.session_state.code_execution_enabled = False
    
    def render_chat_interface(self):
        """Render the main chat interface"""
        st.header("💬 AI Tutor Chat")
        st.markdown("Ask me anything about your studies! I can explain concepts, provide code examples, and help with problem-solving.")
        
        # Chat settings
        with st.expander("⚙️ Chat Settings"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                response_style = st.selectbox(
                    "Response Style",
                    ["Detailed", "Concise", "Step-by-step", "Examples-focused"],
                    help="Choose how you'd like explanations formatted"
                )
            
            with col2:
                include_code = st.checkbox(
                    "Include Code Examples",
                    value=True,
                    help="Include relevant code snippets in responses"
                )
            
            with col3:
                difficulty_level = st.selectbox(
                    "Explanation Level",
                    ["Beginner", "Intermediate", "Advanced"],
                    help="Adjust explanation complexity"
                )
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display chat messages
            self._display_chat_messages()
            
            # Typing indicator
            if st.session_state.typing_indicator:
                with st.chat_message("assistant"):
                    st.markdown("🤔 *Thinking...*")
        
        # Chat input area
        self._render_chat_input(response_style, include_code, difficulty_level)
        
        # Quick action buttons
        self._render_quick_actions()
    
    def _display_chat_messages(self):
        """Display all chat messages with enhanced formatting"""
        for message in st.session_state.chat_messages:
            with st.chat_message(message.role):
                if message.message_type == "code":
                    self._render_code_message(message)
                elif message.message_type == "explanation":
                    self._render_explanation_message(message)
                elif message.message_type == "quiz":
                    self._render_quiz_message(message)
                else:
                    st.markdown(message.content)
                
                # Message metadata
                if message.metadata:
                    with st.expander("📋 Message Details", expanded=False):
                        st.json(message.metadata)
    
    def _render_code_message(self, message: ChatMessage):
        """Render a message containing code"""
        # Parse code snippets from the message
        code_snippets = self._extract_code_snippets(message.content)
        
        if code_snippets:
            for snippet in code_snippets:
                st.code(snippet.code, language=snippet.language)
                if snippet.explanation:
                    st.markdown(f"**Explanation:** {snippet.explanation}")
                
                # Add run button for Python code
                if snippet.language.lower() == "python" and snippet.is_runnable:
                    if st.button(f"▶️ Run Code", key=f"run_{message.id}"):
                        self._execute_code(snippet.code)
        else:
            st.markdown(message.content)
    
    def _render_explanation_message(self, message: ChatMessage):
        """Render an explanation message with enhanced formatting"""
        content = message.content
        
        # Format mathematical expressions
        content = self._format_math_expressions(content)
        
        # Add collapsible sections for long explanations
        if len(content) > 1000:
            sections = content.split('\n\n')
            for i, section in enumerate(sections):
                if i == 0:
                    st.markdown(section)
                else:
                    with st.expander(f"📖 Continue Reading (Part {i})", expanded=False):
                        st.markdown(section)
        else:
            st.markdown(content)
    
    def _render_quiz_message(self, message: ChatMessage):
        """Render an interactive quiz message"""
        quiz_data = message.metadata.get('quiz_data', {})
        
        if quiz_data:
            st.markdown("### 🧠 Quick Quiz")
            question = quiz_data.get('question', '')
            options = quiz_data.get('options', [])
            correct_answer = quiz_data.get('correct_answer', '')
            
            st.markdown(f"**Question:** {question}")
            
            user_answer = st.radio(
                "Choose your answer:",
                options,
                key=f"quiz_{message.id}"
            )
            
            if st.button("Submit Answer", key=f"submit_{message.id}"):
                if user_answer == correct_answer:
                    st.success("🎉 Correct! Well done!")
                else:
                    st.error(f"❌ Not quite. The correct answer is: {correct_answer}")
                
                # Provide explanation
                explanation = quiz_data.get('explanation', '')
                if explanation:
                    st.info(f"💡 **Explanation:** {explanation}")
        else:
            st.markdown(message.content)
    
    def _render_chat_input(self, response_style: str, include_code: bool, difficulty_level: str):
        """Render the chat input area with advanced features"""
        
        # Input methods tabs
        input_tab1, input_tab2 = st.tabs(["💬 Text Input", "🎤 Voice Input"])
        
        with input_tab1:
            # Text input with suggestions
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.chat_input(
                    "Ask me anything about your studies...",
                    key="main_chat_input"
                )
            
            with col2:
                if st.button("📎", help="Attach file or image"):
                    st.info("File attachment feature coming soon!")
        
        with input_tab2:
            st.info("🎤 Voice input feature coming soon!")
            st.markdown("*This will allow you to ask questions using voice commands.*")
        
        # Process user input
        if user_input:
            self._process_user_input(user_input, response_style, include_code, difficulty_level)
    
    def _render_quick_actions(self):
        """Render quick action buttons for common queries"""
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🐍 Python Help"):
                self._handle_quick_action("Explain Python basics and show me a simple example")
        
        with col2:
            if st.button("🧮 Math Problem"):
                self._handle_quick_action("Help me solve a math problem step by step")
        
        with col3:
            if st.button("📚 Study Tips"):
                self._handle_quick_action("Give me effective study tips for my learning style")
        
        with col4:
            if st.button("🔄 Clear Chat"):
                st.session_state.chat_messages = []
                st.rerun()
    
    def _process_user_input(self, user_input: str, response_style: str, 
                          include_code: bool, difficulty_level: str):
        """Process user input and generate AI response"""
        
        # Add user message
        user_message = ChatMessage(
            id=f"user_{len(st.session_state.chat_messages)}",
            role="user",
            content=user_input,
            timestamp=datetime.now(),
            message_type="text",
            metadata={}
        )
        st.session_state.chat_messages.append(user_message)
        
        # Show typing indicator
        st.session_state.typing_indicator = True
        st.rerun()
        
        # Generate AI response
        try:
            response_content, message_type, metadata = self._generate_ai_response(
                user_input, response_style, include_code, difficulty_level
            )
            
            # Add AI response
            ai_message = ChatMessage(
                id=f"assistant_{len(st.session_state.chat_messages)}",
                role="assistant",
                content=response_content,
                timestamp=datetime.now(),
                message_type=message_type,
                metadata=metadata
            )
            st.session_state.chat_messages.append(ai_message)
            
        except Exception as e:
            # Handle errors gracefully
            error_message = ChatMessage(
                id=f"error_{len(st.session_state.chat_messages)}",
                role="assistant",
                content=f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question.",
                timestamp=datetime.now(),
                message_type="text",
                metadata={"error": True}
            )
            st.session_state.chat_messages.append(error_message)
        
        finally:
            # Hide typing indicator
            st.session_state.typing_indicator = False
            st.rerun()
    
    def _generate_ai_response(self, user_input: str, response_style: str, 
                            include_code: bool, difficulty_level: str) -> tuple:
        """Generate AI response with enhanced context and formatting"""
        
        # Build context-aware prompt
        context = self._build_context_prompt(user_input, response_style, include_code, difficulty_level)
        
        # Determine message type based on input
        message_type = self._determine_message_type(user_input)
        
        # Generate response using the educational assistant
        if hasattr(st.session_state, 'user_profile'):
            response = self.assistant.generate_response(context, st.session_state.user_profile)
        else:
            response = self.assistant.generate_response(context, {})
        
        # Process response based on type
        metadata = {}
        
        if message_type == "quiz":
            # Generate quiz if requested
            quiz_data = self._generate_quiz_from_topic(user_input)
            metadata['quiz_data'] = quiz_data
            response += f"\n\n{self._format_quiz_response(quiz_data)}"
        
        elif message_type == "code" and include_code:
            # Enhance code examples
            response = self._enhance_code_examples(response)
        
        return response, message_type, metadata
    
    def _build_context_prompt(self, user_input: str, response_style: str, 
                            include_code: bool, difficulty_level: str) -> str:
        """Build a context-aware prompt for the AI"""
        
        # Get user profile context
        user_context = ""
        if hasattr(st.session_state, 'user_profile') and st.session_state.user_profile:
            profile = st.session_state.user_profile
            user_context = f"""
            User Profile Context:
            - Learning Style: {getattr(profile, 'learning_style', 'Unknown')}
            - Subjects: {getattr(profile, 'subjects', [])}
            - Name: {getattr(profile, 'name', 'Student')}
            """
        
        # Build the enhanced prompt
        prompt = f"""
        {user_context}
        
        Response Guidelines:
        - Style: {response_style}
        - Level: {difficulty_level}
        - Include Code: {include_code}
        
        User Question: {user_input}
        
        Please provide a helpful, educational response that:
        1. Addresses the user's question directly
        2. Matches the requested style and difficulty level
        3. Includes practical examples when appropriate
        4. Uses clear, engaging language
        {"5. Includes relevant code snippets with explanations" if include_code else ""}
        """
        
        return prompt
    
    def _determine_message_type(self, user_input: str) -> str:
        """Determine the type of message based on user input"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["quiz", "test", "question", "assess"]):
            return "quiz"
        elif any(word in input_lower for word in ["code", "program", "function", "script", "python", "javascript"]):
            return "code"
        elif any(word in input_lower for word in ["explain", "how", "what", "why", "concept"]):
            return "explanation"
        else:
            return "text"
    
    def _extract_code_snippets(self, content: str) -> List[CodeSnippet]:
        """Extract code snippets from message content"""
        snippets = []
        
        # Pattern to match code blocks
        code_pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.findall(code_pattern, content, re.DOTALL)
        
        for language, code in matches:
            language = language or "text"
            snippets.append(CodeSnippet(
                language=language,
                code=code.strip(),
                explanation="",
                is_runnable=language.lower() in ["python", "javascript"]
            ))
        
        return snippets
    
    def _format_math_expressions(self, content: str) -> str:
        """Format mathematical expressions using LaTeX"""
        # Simple LaTeX formatting for common math expressions
        content = re.sub(r'\$([^$]+)\$', r'$$\1$$', content)
        return content
    
    def _execute_code(self, code: str):
        """Execute Python code safely (demo version)"""
        st.info("🔒 Code execution is disabled for security. This is a demonstration of the feature.")
        st.code(f"# Would execute:\n{code}", language="python")
    
    def _handle_quick_action(self, action_text: str):
        """Handle quick action button clicks"""
        self._process_user_input(action_text, "Detailed", True, "Intermediate")
    
    def _generate_quiz_from_topic(self, topic: str) -> Dict[str, Any]:
        """Generate a quiz based on the topic"""
        # This is a simplified version - in a real implementation,
        # this would use AI to generate contextual quizzes
        
        sample_quizzes = {
            "python": {
                "question": "What is the correct way to define a function in Python?",
                "options": [
                    "function myFunc():",
                    "def myFunc():",
                    "func myFunc():",
                    "define myFunc():"
                ],
                "correct_answer": "def myFunc():",
                "explanation": "In Python, functions are defined using the 'def' keyword followed by the function name and parentheses."
            },
            "math": {
                "question": "What is the result of 2³?",
                "options": ["6", "8", "9", "12"],
                "correct_answer": "8",
                "explanation": "2³ means 2 × 2 × 2 = 8"
            }
        }
        
        # Simple topic matching
        topic_lower = topic.lower()
        if "python" in topic_lower:
            return sample_quizzes["python"]
        elif any(word in topic_lower for word in ["math", "algebra", "calculation"]):
            return sample_quizzes["math"]
        else:
            return {
                "question": f"What would you like to learn more about regarding {topic}?",
                "options": ["Basic concepts", "Advanced topics", "Practical examples", "Related subjects"],
                "correct_answer": "Basic concepts",
                "explanation": "Starting with basic concepts provides a solid foundation for learning."
            }
    
    def _format_quiz_response(self, quiz_data: Dict[str, Any]) -> str:
        """Format quiz data into a readable response"""
        if not quiz_data:
            return ""
        
        return f"""
        
        ### 🧠 Quick Quiz
        
        **{quiz_data.get('question', '')}**
        
        Choose from the options above to test your understanding!
        """
    
    def _enhance_code_examples(self, response: str) -> str:
        """Enhance code examples in the response"""
        # Add syntax highlighting hints and explanations
        enhanced = response
        
        # Add helpful comments to code blocks
        code_blocks = re.findall(r'```python\n(.*?)\n```', enhanced, re.DOTALL)
        for code_block in code_blocks:
            if "# " not in code_block:  # If no comments exist
                # Add a simple comment
                commented_code = f"# Example code:\n{code_block}"
                enhanced = enhanced.replace(code_block, commented_code)
        
        return enhanced
    
    def get_chat_statistics(self) -> Dict[str, Any]:
        """Get statistics about the current chat session"""
        messages = st.session_state.chat_messages
        
        return {
            "total_messages": len(messages),
            "user_messages": len([m for m in messages if m.role == "user"]),
            "assistant_messages": len([m for m in messages if m.role == "assistant"]),
            "code_messages": len([m for m in messages if m.message_type == "code"]),
            "quiz_messages": len([m for m in messages if m.message_type == "quiz"]),
            "session_duration": (datetime.now() - messages[0].timestamp).total_seconds() / 60 if messages else 0
        }
    
    def export_chat_history(self) -> str:
        """Export chat history as JSON"""
        chat_data = []
        for message in st.session_state.chat_messages:
            chat_data.append({
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "message_type": message.message_type,
                "metadata": message.metadata
            })
        
        return json.dumps(chat_data, indent=2)