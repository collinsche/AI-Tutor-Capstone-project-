#!/usr/bin/env python3
"""
AI-Powered Content Generation Tools for Educational Assistant
Generates summaries, flashcards, and practice problems using Grok AI
"""

import streamlit as st
import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from educational_assistant import EducationalAssistant

class ContentType(Enum):
    SUMMARY = "summary"
    FLASHCARD = "flashcard"
    PRACTICE_PROBLEM = "practice_problem"
    STUDY_GUIDE = "study_guide"
    CONCEPT_MAP = "concept_map"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class ContentItem:
    """Base content item structure"""
    content_id: str
    content_type: ContentType
    subject: str
    topic: str
    difficulty: DifficultyLevel
    title: str
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime
    user_id: str

@dataclass
class Summary:
    """Summary content structure"""
    title: str
    key_points: List[str]
    detailed_explanation: str
    examples: List[str]
    related_topics: List[str]
    estimated_read_time: int

@dataclass
class Flashcard:
    """Flashcard content structure"""
    front: str
    back: str
    hint: str
    difficulty_level: str
    tags: List[str]
    example: str

@dataclass
class PracticeProblem:
    """Practice problem content structure"""
    problem_statement: str
    solution: str
    step_by_step: List[str]
    hints: List[str]
    similar_problems: List[str]
    concepts_tested: List[str]

class ContentGenerator:
    """AI-powered content generation engine"""
    
    def __init__(self, educational_assistant: EducationalAssistant):
        self.ai_assistant = educational_assistant
        self.content_templates = self._initialize_templates()
        
    def _initialize_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize content generation templates"""
        return {
            ContentType.SUMMARY.value: {
                "system_prompt": "You are an expert educational content creator specializing in creating clear, concise summaries.",
                "user_prompt_template": """
                Create a comprehensive summary for the topic: {topic} in {subject}.
                Difficulty level: {difficulty}
                Target audience: {audience}
                
                Format as JSON:
                {{
                    "title": "Clear, engaging title",
                    "key_points": ["point1", "point2", "point3"],
                    "detailed_explanation": "2-3 paragraph explanation",
                    "examples": ["example1", "example2"],
                    "related_topics": ["topic1", "topic2"],
                    "estimated_read_time": 5
                }}
                
                Make it educational, engaging, and appropriate for the difficulty level.
                """
            },
            ContentType.FLASHCARD.value: {
                "system_prompt": "You are an expert at creating effective flashcards for learning and memorization.",
                "user_prompt_template": """
                Create a flashcard for the topic: {topic} in {subject}.
                Difficulty level: {difficulty}
                Focus area: {focus_area}
                
                Format as JSON:
                {{
                    "front": "Question or prompt (concise)",
                    "back": "Answer or explanation (clear and complete)",
                    "hint": "Helpful hint without giving away the answer",
                    "difficulty_level": "{difficulty}",
                    "tags": ["tag1", "tag2", "tag3"],
                    "example": "Practical example or application"
                }}
                
                Make the front side challenging but fair, and the back side comprehensive but concise.
                """
            },
            ContentType.PRACTICE_PROBLEM.value: {
                "system_prompt": "You are an expert educator creating practice problems that help students learn through application.",
                "user_prompt_template": """
                Create a practice problem for the topic: {topic} in {subject}.
                Difficulty level: {difficulty}
                Problem type: {problem_type}
                
                Format as JSON:
                {{
                    "problem_statement": "Clear problem description",
                    "solution": "Complete solution",
                    "step_by_step": ["step1", "step2", "step3"],
                    "hints": ["hint1", "hint2"],
                    "similar_problems": ["problem1", "problem2"],
                    "concepts_tested": ["concept1", "concept2"]
                }}
                
                Make it educational, challenging but solvable, with clear explanations.
                """
            }
        }
    
    def generate_summary(self, topic: str, subject: str, difficulty: DifficultyLevel,
                        audience: str = "students", user_id: str = "default") -> ContentItem:
        """Generate an AI-powered topic summary"""
        try:
            template = self.content_templates[ContentType.SUMMARY.value]
            
            prompt = template["user_prompt_template"].format(
                topic=topic,
                subject=subject,
                difficulty=difficulty.value,
                audience=audience
            )
            
            # Use the educational assistant's generate_response method instead of direct client access
            full_prompt = f"{template['system_prompt']}\n\nUser: {prompt}"
            
            # Create a temporary user profile for content generation
            from user_profile import UserProfile
            temp_profile = UserProfile()
            temp_profile.learning_style = "Reading/Writing"  # Default for content generation
            temp_profile.academic_level = difficulty.value
            
            # Check if AI assistant is properly configured
            if not hasattr(self.ai_assistant, 'config') or not self.ai_assistant.config:
                st.error("AI configuration not found")
                return None
                
            # Check if API key is configured
            if not self.ai_assistant.api_key and not self.ai_assistant.config.use_demo_mode:
                st.error("AI API key not configured")
                return None
            
            response_text = self.ai_assistant.generate_response(full_prompt, temp_profile)
            
            # Check if response was generated successfully
            if not response_text or response_text.strip() == "":
                st.error("Failed to generate content response")
                return None
            
            # Try to parse JSON response, fallback to structured text if needed
            try:
                content_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: create structured content from text response
                content_data = self._parse_text_to_summary_structure(response_text, topic)
            
            summary = Summary(
                title=content_data.get("title", f"{topic} Summary"),
                key_points=content_data.get("key_points", [f"Key concepts about {topic}"]),
                detailed_explanation=content_data.get("detailed_explanation", response_text[:500]),
                examples=content_data.get("examples", [f"Example applications of {topic}"]),
                related_topics=content_data.get("related_topics", [subject]),
                estimated_read_time=content_data.get("estimated_read_time", 5)
            )
            
            content_item = ContentItem(
                content_id=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                content_type=ContentType.SUMMARY,
                subject=subject,
                topic=topic,
                difficulty=difficulty,
                title=summary.title,
                content=asdict(summary),
                metadata={
                    "audience": audience,
                    "generated_by": "ai",
                    "model": self.ai_assistant.config.model_name
                },
                created_at=datetime.now(),
                user_id=user_id
            )
            
            return content_item
            
        except Exception as e:
            st.error(f"Failed to generate summary: {e}")
            return None
    
    def _parse_text_to_summary_structure(self, text: str, topic: str) -> Dict[str, Any]:
        """Parse plain text response into summary structure"""
        lines = text.split('\n')
        
        # Extract key information from text
        title = f"{topic} Summary"
        key_points = []
        detailed_explanation = ""
        examples = []
        
        current_section = "explanation"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for key points indicators
            if any(indicator in line.lower() for indicator in ["key point", "important", "main concept", "•", "-"]):
                key_points.append(line.replace("•", "").replace("-", "").strip())
                current_section = "points"
            elif any(indicator in line.lower() for indicator in ["example", "for instance", "such as"]):
                examples.append(line)
                current_section = "examples"
            else:
                if current_section == "explanation" and len(detailed_explanation) < 300:
                    detailed_explanation += line + " "
        
        # Ensure we have at least some content
        if not detailed_explanation:
            detailed_explanation = text[:300] + "..." if len(text) > 300 else text
        
        if not key_points:
            key_points = [f"Understanding {topic}", f"Applications of {topic}", f"Key concepts in {topic}"]
        
        if not examples:
            examples = [f"Practical applications of {topic}"]
        
        return {
            "title": title,
            "key_points": key_points,
            "detailed_explanation": detailed_explanation.strip(),
            "examples": examples,
            "related_topics": [topic],
            "estimated_read_time": max(2, len(detailed_explanation) // 200)
        }
    
    def generate_flashcard_set(self, topic: str, subject: str, difficulty: DifficultyLevel,
                              count: int = 5, focus_areas: List[str] = None,
                              user_id: str = "default") -> List[ContentItem]:
        """Generate a set of flashcards for a topic"""
        flashcards = []
        focus_areas = focus_areas or ["key concepts", "definitions", "applications", "examples"]
        
        for i in range(count):
            focus_area = focus_areas[i % len(focus_areas)]
            flashcard = self.generate_single_flashcard(topic, subject, difficulty, focus_area, user_id)
            if flashcard:
                flashcards.append(flashcard)
        
        return flashcards
    
    def generate_single_flashcard(self, topic: str, subject: str, difficulty: DifficultyLevel,
                                 focus_area: str = "key concepts", user_id: str = "default") -> ContentItem:
        """Generate a single flashcard"""
        try:
            template = self.content_templates[ContentType.FLASHCARD.value]
            
            prompt = template["user_prompt_template"].format(
                topic=topic,
                subject=subject,
                difficulty=difficulty.value,
                focus_area=focus_area
            )
            
            # Use the educational assistant's generate_response method
            full_prompt = f"{template['system_prompt']}\n\nUser: {prompt}"
            
            # Create a temporary user profile for content generation
            from user_profile import UserProfile
            temp_profile = UserProfile()
            temp_profile.learning_style = "Reading/Writing"
            temp_profile.academic_level = difficulty.value
            
            response_text = self.ai_assistant.generate_response(full_prompt, temp_profile)
            
            # Try to parse JSON response, fallback to structured text if needed
            try:
                content_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: create structured flashcard from text response
                content_data = self._parse_text_to_flashcard_structure(response_text, topic, focus_area)
            
            flashcard = Flashcard(
                front=content_data.get("front", f"What is {topic}?"),
                back=content_data.get("back", f"Key concept about {topic}"),
                hint=content_data.get("hint", f"Think about {focus_area}"),
                difficulty_level=content_data.get("difficulty_level", difficulty.value),
                tags=content_data.get("tags", [topic, subject]),
                example=content_data.get("example", f"Example of {topic}")
            )
            
            content_item = ContentItem(
                content_id=f"flashcard_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
                content_type=ContentType.FLASHCARD,
                subject=subject,
                topic=topic,
                difficulty=difficulty,
                title=f"Flashcard: {topic}",
                content=asdict(flashcard),
                metadata={
                    "focus_area": focus_area,
                    "generated_by": "ai",
                    "model": self.ai_assistant.config.model_name
                },
                created_at=datetime.now(),
                user_id=user_id
            )
            
            return content_item
            
        except Exception as e:
            st.error(f"Failed to generate flashcard: {e}")
            return None
    
    def _parse_text_to_flashcard_structure(self, text: str, topic: str, focus_area: str) -> Dict[str, Any]:
        """Parse plain text response into flashcard structure"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Default structure
        flashcard_data = {
            "front": f"What is {topic}?",
            "back": f"Key concept about {topic}",
            "hint": f"Think about {focus_area}",
            "difficulty_level": "intermediate",
            "tags": [topic],
            "example": f"Example of {topic}"
        }
        
        # Try to extract structured information
        current_field = None
        for line in lines:
            line_lower = line.lower()
            
            if any(indicator in line_lower for indicator in ["question:", "front:", "q:"]):
                current_field = "front"
                flashcard_data["front"] = line.split(":", 1)[-1].strip()
            elif any(indicator in line_lower for indicator in ["answer:", "back:", "a:"]):
                current_field = "back"
                flashcard_data["back"] = line.split(":", 1)[-1].strip()
            elif "hint:" in line_lower:
                current_field = "hint"
                flashcard_data["hint"] = line.split(":", 1)[-1].strip()
            elif "example:" in line_lower:
                current_field = "example"
                flashcard_data["example"] = line.split(":", 1)[-1].strip()
            elif current_field and not any(indicator in line_lower for indicator in ["question:", "answer:", "hint:", "example:"]):
                # Continue building the current field
                flashcard_data[current_field] += " " + line
        
        # If we couldn't extract proper front/back, use the text content
        if flashcard_data["front"] == f"What is {topic}?" and len(lines) > 0:
            flashcard_data["front"] = f"What is {topic}?"
            flashcard_data["back"] = " ".join(lines[:3]) if len(lines) >= 3 else text[:200]
        
        return flashcard_data

    def generate_practice_problems(self, topic: str, subject: str, difficulty: DifficultyLevel,
                                 count: int = 3, problem_types: List[str] = None,
                                 user_id: str = "default") -> List[ContentItem]:
        """Generate practice problems for a topic"""
        problems = []
        problem_types = problem_types or ["application", "analysis", "synthesis"]
        
        for i in range(count):
            problem_type = problem_types[i % len(problem_types)]
            problem = self.generate_single_practice_problem(topic, subject, difficulty, problem_type, user_id)
            if problem:
                problems.append(problem)
        
        return problems
    
    def generate_single_practice_problem(self, topic: str, subject: str, difficulty: DifficultyLevel,
                                       problem_type: str = "application", user_id: str = "default") -> ContentItem:
        """Generate a single practice problem"""
        try:
            template = self.content_templates[ContentType.PRACTICE_PROBLEM.value]
            
            prompt = template["user_prompt_template"].format(
                topic=topic,
                subject=subject,
                difficulty=difficulty.value,
                problem_type=problem_type
            )
            
            # Use the educational assistant's generate_response method
            full_prompt = f"{template['system_prompt']}\n\nUser: {prompt}"
            
            # Create a temporary user profile for content generation
            from user_profile import UserProfile
            temp_profile = UserProfile()
            temp_profile.learning_style = "Reading/Writing"
            temp_profile.academic_level = difficulty.value
            
            response_text = self.ai_assistant.generate_response(full_prompt, temp_profile)
            
            # Try to parse JSON response, fallback to structured text if needed
            try:
                content_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: create structured content from text response
                content_data = self._parse_text_to_practice_problem_structure(response_text, topic)
            
            practice_problem = PracticeProblem(
                problem_statement=content_data.get("problem_statement", f"Solve this problem about {topic}"),
                solution=content_data.get("solution", f"Solution for {topic} problem"),
                step_by_step=content_data.get("step_by_step", [f"Step 1: Analyze the {topic} problem"]),
                hints=content_data.get("hints", [f"Consider the key concepts of {topic}"]),
                similar_problems=content_data.get("similar_problems", [f"Related {topic} problems"]),
                concepts_tested=content_data.get("concepts_tested", [topic])
            )
            
            content_item = ContentItem(
                content_id=f"problem_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
                content_type=ContentType.PRACTICE_PROBLEM,
                subject=subject,
                topic=topic,
                difficulty=difficulty,
                title=f"Practice Problem: {topic}",
                content=asdict(practice_problem),
                metadata={
                    "problem_type": problem_type,
                    "generated_by": "ai",
                    "model": self.ai_assistant.config.model_name
                },
                created_at=datetime.now(),
                user_id=user_id
            )
            
            return content_item
            
        except Exception as e:
            st.error(f"Failed to generate practice problem: {e}")
            return None
    
    def _parse_text_to_practice_problem_structure(self, text: str, topic: str) -> Dict[str, Any]:
        """Parse plain text response into practice problem structure"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Default structure
        problem_data = {
            "problem_statement": f"Solve this problem about {topic}",
            "solution": f"Solution for {topic} problem",
            "step_by_step": [f"Step 1: Analyze the {topic} problem"],
            "hints": [f"Consider the key concepts of {topic}"],
            "similar_problems": [f"Related {topic} problems"],
            "concepts_tested": [topic]
        }
        
        # Try to extract structured information
        current_field = None
        current_list = []
        
        for line in lines:
            line_lower = line.lower()
            
            if any(indicator in line_lower for indicator in ["problem:", "question:", "statement:"]):
                current_field = "problem_statement"
                problem_data["problem_statement"] = line.split(":", 1)[-1].strip()
            elif any(indicator in line_lower for indicator in ["solution:", "answer:"]):
                current_field = "solution"
                problem_data["solution"] = line.split(":", 1)[-1].strip()
            elif "step" in line_lower and any(char.isdigit() for char in line):
                if current_field != "step_by_step":
                    current_field = "step_by_step"
                    problem_data["step_by_step"] = []
                problem_data["step_by_step"].append(line)
            elif "hint" in line_lower:
                if current_field != "hints":
                    current_field = "hints"
                    problem_data["hints"] = []
                problem_data["hints"].append(line.replace("hint:", "").strip())
            elif current_field and current_field in ["step_by_step", "hints"] and line.startswith(("-", "•", "*")):
                problem_data[current_field].append(line.lstrip("-•* "))
            elif current_field and current_field in ["problem_statement", "solution"]:
                problem_data[current_field] += " " + line
        
        # Ensure we have at least basic content
        if problem_data["problem_statement"] == f"Solve this problem about {topic}" and len(lines) > 0:
            problem_data["problem_statement"] = lines[0] if lines else f"What is {topic}?"
            if len(lines) > 1:
                problem_data["solution"] = " ".join(lines[1:3])
        
        return problem_data
    
    def generate_study_guide(self, topics: List[str], subject: str, difficulty: DifficultyLevel,
                           user_id: str = "default") -> ContentItem:
        """Generate a comprehensive study guide for multiple topics"""
        try:
            topics_str = ", ".join(topics)
            
            prompt = f"""
            Create a comprehensive study guide for {subject} covering these topics: {topics_str}
            Difficulty level: {difficulty.value}
            
            Format as JSON:
            {{
                "title": "Study Guide Title",
                "overview": "Brief overview of what will be covered",
                "sections": [
                    {{
                        "topic": "topic name",
                        "key_concepts": ["concept1", "concept2"],
                        "important_formulas": ["formula1", "formula2"],
                        "study_tips": ["tip1", "tip2"],
                        "practice_suggestions": ["suggestion1", "suggestion2"]
                    }}
                ],
                "review_checklist": ["item1", "item2", "item3"],
                "additional_resources": ["resource1", "resource2"],
                "estimated_study_time": "2-3 hours"
            }}
            
            Make it comprehensive and well-organized for effective studying.
            """
            
            # Use the educational assistant's generate_response method
            full_prompt = f"You are an expert study guide creator helping students organize their learning.\n\nUser: {prompt}"
            
            # Create a temporary user profile for content generation
            from user_profile import UserProfile
            temp_profile = UserProfile()
            temp_profile.learning_style = "Reading/Writing"
            temp_profile.academic_level = difficulty.value
            
            response_text = self.ai_assistant.generate_response(full_prompt, temp_profile)
            
            # Try to parse JSON response, fallback to structured text if needed
            try:
                content_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: create structured study guide from text response
                content_data = self._parse_text_to_study_guide_structure(response_text, topics, subject)
            
            content_item = ContentItem(
                content_id=f"study_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                content_type=ContentType.STUDY_GUIDE,
                subject=subject,
                topic=", ".join(topics),
                difficulty=difficulty,
                title=content_data.get("title", f"Study Guide: {subject}"),
                content=content_data,
                metadata={
                    "topics_covered": len(topics),
                    "generated_by": "ai",
                    "model": self.ai_assistant.config.model_name
                },
                created_at=datetime.now(),
                user_id=user_id
            )
            
            return content_item
            
        except Exception as e:
            st.error(f"Failed to generate study guide: {e}")
            return None
    
    def _parse_text_to_study_guide_structure(self, text: str, topics: List[str], subject: str) -> Dict[str, Any]:
        """Parse plain text response into study guide structure"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Default structure
        study_guide_data = {
            "title": f"Study Guide: {subject}",
            "overview": f"Comprehensive study guide covering {', '.join(topics)}",
            "sections": [],
            "review_checklist": [f"Review {topic}" for topic in topics],
            "additional_resources": [f"Additional resources for {subject}"],
            "estimated_study_time": "2-3 hours"
        }
        
        # Create sections for each topic
        for topic in topics:
            section = {
                "topic": topic,
                "key_concepts": [f"Key concepts of {topic}"],
                "important_formulas": [f"Formulas related to {topic}"],
                "study_tips": [f"Study tips for {topic}"],
                "practice_suggestions": [f"Practice problems for {topic}"]
            }
            study_guide_data["sections"].append(section)
        
        # Try to extract more detailed information from text
        current_section = None
        current_field = None
        
        for line in lines:
            line_lower = line.lower()
            
            # Look for topic sections
            for topic in topics:
                if topic.lower() in line_lower and any(indicator in line_lower for indicator in ["section", "topic", "chapter"]):
                    current_section = next((s for s in study_guide_data["sections"] if s["topic"].lower() == topic.lower()), None)
                    break
            
            if current_section:
                if any(indicator in line_lower for indicator in ["key concept", "concept", "important"]):
                    current_field = "key_concepts"
                    if ":" in line:
                        current_section["key_concepts"].append(line.split(":", 1)[-1].strip())
                elif any(indicator in line_lower for indicator in ["formula", "equation"]):
                    current_field = "important_formulas"
                    if ":" in line:
                        current_section["important_formulas"].append(line.split(":", 1)[-1].strip())
                elif any(indicator in line_lower for indicator in ["tip", "study", "remember"]):
                    current_field = "study_tips"
                    if ":" in line:
                        current_section["study_tips"].append(line.split(":", 1)[-1].strip())
                elif any(indicator in line_lower for indicator in ["practice", "exercise", "problem"]):
                    current_field = "practice_suggestions"
                    if ":" in line:
                        current_section["practice_suggestions"].append(line.split(":", 1)[-1].strip())
        
        return study_guide_data

class ContentInterface:
    """Streamlit interface for content generation tools"""
    
    def __init__(self, content_generator: ContentGenerator):
        self.content_generator = content_generator
        
        # Initialize session state for generated content
        if 'generated_content' not in st.session_state:
            st.session_state.generated_content = []
    
    def render_content_generator(self, user_id: str):
        """Render the main content generation interface"""
        st.header("🎯 AI Content Generator")
        st.markdown("Generate personalized learning materials using AI")
        
        # Content type selection
        content_type = st.selectbox(
            "What would you like to generate?",
            options=["Summary", "Flashcards", "Practice Problems", "Study Guide"],
            help="Choose the type of content you want to create"
        )
        
        # Common inputs
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox(
                "Subject",
                options=["Python Programming", "Mathematics", "Physics", "Chemistry", "Biology", "History", "Literature"],
                help="Select the subject area"
            )
        
        with col2:
            difficulty = st.selectbox(
                "Difficulty Level",
                options=["Beginner", "Intermediate", "Advanced"],
                help="Choose appropriate difficulty level"
            )
        
        topic = st.text_input(
            "Topic",
            placeholder="e.g., Variables and Data Types, Quadratic Equations, etc.",
            help="Enter the specific topic you want to focus on"
        )
        
        if topic:
            difficulty_enum = DifficultyLevel(difficulty.lower())
            
            if content_type == "Summary":
                self._render_summary_generator(topic, subject, difficulty_enum, user_id)
            elif content_type == "Flashcards":
                self._render_flashcard_generator(topic, subject, difficulty_enum, user_id)
            elif content_type == "Practice Problems":
                self._render_practice_problem_generator(topic, subject, difficulty_enum, user_id)
            elif content_type == "Study Guide":
                self._render_study_guide_generator(topic, subject, difficulty_enum, user_id)
        
        # Display generated content
        self._render_generated_content()
    
    def _render_summary_generator(self, topic: str, subject: str, difficulty: DifficultyLevel, user_id: str):
        """Render summary generation interface"""
        st.subheader("📝 Generate Summary")
        
        audience = st.selectbox(
            "Target Audience",
            options=["Students", "Professionals", "General Public"],
            help="Who is this summary for?"
        )
        
        if st.button("Generate Summary", type="primary"):
            with st.spinner("Generating summary..."):
                summary = self.content_generator.generate_summary(
                    topic, subject, difficulty, audience.lower(), user_id
                )
                
                if summary:
                    st.session_state.generated_content.append(summary)
                    st.success("Summary generated successfully!")
                    st.rerun()
    
    def _render_flashcard_generator(self, topic: str, subject: str, difficulty: DifficultyLevel, user_id: str):
        """Render flashcard generation interface"""
        st.subheader("🃏 Generate Flashcards")
        
        col1, col2 = st.columns(2)
        
        with col1:
            count = st.number_input("Number of flashcards", min_value=1, max_value=20, value=5)
        
        with col2:
            focus_areas = st.multiselect(
                "Focus Areas",
                options=["Key Concepts", "Definitions", "Applications", "Examples", "Formulas", "Facts"],
                default=["Key Concepts", "Definitions"],
                help="What aspects should the flashcards focus on?"
            )
        
        if st.button("Generate Flashcards", type="primary"):
            with st.spinner(f"Generating {count} flashcards..."):
                flashcards = self.content_generator.generate_flashcard_set(
                    topic, subject, difficulty, count, 
                    [area.lower() for area in focus_areas], user_id
                )
                
                if flashcards:
                    st.session_state.generated_content.extend(flashcards)
                    st.success(f"Generated {len(flashcards)} flashcards successfully!")
                    st.rerun()
    
    def _render_practice_problem_generator(self, topic: str, subject: str, difficulty: DifficultyLevel, user_id: str):
        """Render practice problem generation interface"""
        st.subheader("🧮 Generate Practice Problems")
        
        col1, col2 = st.columns(2)
        
        with col1:
            count = st.number_input("Number of problems", min_value=1, max_value=10, value=3)
        
        with col2:
            problem_types = st.multiselect(
                "Problem Types",
                options=["Application", "Analysis", "Synthesis", "Evaluation", "Conceptual", "Computational"],
                default=["Application", "Analysis"],
                help="What types of problems should be generated?"
            )
        
        if st.button("Generate Practice Problems", type="primary"):
            with st.spinner(f"Generating {count} practice problems..."):
                problems = self.content_generator.generate_practice_problems(
                    topic, subject, difficulty, count,
                    [ptype.lower() for ptype in problem_types], user_id
                )
                
                if problems:
                    st.session_state.generated_content.extend(problems)
                    st.success(f"Generated {len(problems)} practice problems successfully!")
                    st.rerun()
    
    def _render_study_guide_generator(self, topic: str, subject: str, difficulty: DifficultyLevel, user_id: str):
        """Render study guide generation interface"""
        st.subheader("📚 Generate Study Guide")
        
        additional_topics = st.text_area(
            "Additional Topics (one per line)",
            placeholder="Enter additional topics to include in the study guide",
            help="Add more topics to create a comprehensive study guide"
        )
        
        topics = [topic]
        if additional_topics:
            topics.extend([t.strip() for t in additional_topics.split('\n') if t.strip()])
        
        st.info(f"Study guide will cover: {', '.join(topics)}")
        
        if st.button("Generate Study Guide", type="primary"):
            with st.spinner("Generating comprehensive study guide..."):
                study_guide = self.content_generator.generate_study_guide(
                    topics, subject, difficulty, user_id
                )
                
                if study_guide:
                    st.session_state.generated_content.append(study_guide)
                    st.success("Study guide generated successfully!")
                    st.rerun()
    
    def _render_generated_content(self):
        """Display generated content"""
        if not st.session_state.generated_content:
            return
        
        st.markdown("---")
        st.subheader("📋 Generated Content")
        
        # Filter and sort content
        content_items = sorted(
            st.session_state.generated_content,
            key=lambda x: x.created_at,
            reverse=True
        )
        
        for item in content_items:
            with st.expander(f"{item.content_type.value.title()}: {item.title}"):
                self._render_content_item(item)
    
    def _render_content_item(self, item: ContentItem):
        """Render individual content item"""
        # Header info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Subject:** {item.subject}")
        with col2:
            st.write(f"**Difficulty:** {item.difficulty.value.title()}")
        with col3:
            st.write(f"**Created:** {item.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        # Content based on type
        if item.content_type == ContentType.SUMMARY:
            self._render_summary_content(item.content)
        elif item.content_type == ContentType.FLASHCARD:
            self._render_flashcard_content(item.content)
        elif item.content_type == ContentType.PRACTICE_PROBLEM:
            self._render_practice_problem_content(item.content)
        elif item.content_type == ContentType.STUDY_GUIDE:
            self._render_study_guide_content(item.content)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📥 Export", key=f"export_{item.content_id}"):
                st.download_button(
                    "Download as JSON",
                    data=json.dumps(asdict(item), indent=2, default=str),
                    file_name=f"{item.content_type.value}_{item.content_id}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button(f"🔄 Regenerate", key=f"regen_{item.content_id}"):
                st.info("Regeneration feature would be implemented here")
        
        with col3:
            if st.button(f"🗑️ Delete", key=f"delete_{item.content_id}"):
                st.session_state.generated_content = [
                    c for c in st.session_state.generated_content 
                    if c.content_id != item.content_id
                ]
                st.rerun()
    
    def _render_summary_content(self, content: Dict[str, Any]):
        """Render summary content"""
        st.markdown(f"**📖 {content['title']}**")
        st.markdown(f"*Estimated reading time: {content['estimated_read_time']} minutes*")
        
        st.markdown("**Key Points:**")
        for point in content['key_points']:
            st.markdown(f"• {point}")
        
        st.markdown("**Detailed Explanation:**")
        st.markdown(content['detailed_explanation'])
        
        if content['examples']:
            st.markdown("**Examples:**")
            for example in content['examples']:
                st.markdown(f"• {example}")
        
        if content['related_topics']:
            st.markdown("**Related Topics:**")
            st.markdown(", ".join(content['related_topics']))
    
    def _render_flashcard_content(self, content: Dict[str, Any]):
        """Render flashcard content"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔍 Front (Question):**")
            st.info(content['front'])
            
            if content['hint']:
                with st.expander("💡 Hint"):
                    st.write(content['hint'])
        
        with col2:
            st.markdown("**✅ Back (Answer):**")
            st.success(content['back'])
            
            if content['example']:
                st.markdown("**Example:**")
                st.write(content['example'])
        
        if content['tags']:
            st.markdown(f"**Tags:** {', '.join(content['tags'])}")
    
    def _render_practice_problem_content(self, content: Dict[str, Any]):
        """Render practice problem content"""
        st.markdown("**📝 Problem Statement:**")
        st.markdown(content['problem_statement'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("💡 Hints"):
                for i, hint in enumerate(content['hints'], 1):
                    st.write(f"{i}. {hint}")
        
        with col2:
            with st.expander("✅ Solution"):
                st.markdown("**Answer:**")
                st.write(content['solution'])
                
                if content['step_by_step']:
                    st.markdown("**Step-by-step:**")
                    for i, step in enumerate(content['step_by_step'], 1):
                        st.write(f"{i}. {step}")
        
        if content['concepts_tested']:
            st.markdown(f"**Concepts Tested:** {', '.join(content['concepts_tested'])}")
    
    def _render_study_guide_content(self, content: Dict[str, Any]):
        """Render study guide content"""
        st.markdown(f"**📚 {content['title']}**")
        st.markdown(f"*Estimated study time: {content['estimated_study_time']}*")
        
        st.markdown("**Overview:**")
        st.markdown(content['overview'])
        
        st.markdown("**Study Sections:**")
        for section in content['sections']:
            with st.expander(f"📖 {section['topic']}"):
                st.markdown("**Key Concepts:**")
                for concept in section['key_concepts']:
                    st.markdown(f"• {concept}")
                
                if section.get('important_formulas'):
                    st.markdown("**Important Formulas:**")
                    for formula in section['important_formulas']:
                        st.code(formula)
                
                st.markdown("**Study Tips:**")
                for tip in section['study_tips']:
                    st.markdown(f"💡 {tip}")
        
        if content['review_checklist']:
            st.markdown("**Review Checklist:**")
            for item in content['review_checklist']:
                st.checkbox(item, key=f"checklist_{hash(item)}")
        
        if content['additional_resources']:
            st.markdown("**Additional Resources:**")
            for resource in content['additional_resources']:
                st.markdown(f"• {resource}")