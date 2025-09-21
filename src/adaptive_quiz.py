#!/usr/bin/env python3
"""
Adaptive Quiz System for AI Educational Assistant
Implements dynamic quizzes with automatic difficulty adjustment and AI-generated feedback using Grok
"""

import streamlit as st
import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from educational_assistant import EducationalAssistant

class DifficultyLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    CODE_COMPLETION = "code_completion"
    FILL_BLANK = "fill_blank"

@dataclass
class QuizQuestion:
    """Quiz question data structure"""
    question_id: str
    subject: str
    topic: str
    question_text: str
    question_type: QuestionType
    difficulty_level: DifficultyLevel
    options: List[str]  # For multiple choice
    correct_answer: str
    explanation: str
    hints: List[str]
    estimated_time: int  # seconds
    tags: List[str]
    metadata: Dict[str, Any]

@dataclass
class QuizAttempt:
    """Quiz attempt tracking"""
    attempt_id: str
    user_id: str
    question_id: str
    user_answer: str
    is_correct: bool
    time_taken: int
    hints_used: int
    difficulty_at_attempt: DifficultyLevel
    timestamp: datetime
    confidence_level: int  # 1-5 scale

@dataclass
class QuizSession:
    """Quiz session management"""
    session_id: str
    user_id: str
    subject: str
    start_time: datetime
    current_difficulty: DifficultyLevel
    questions_answered: int
    correct_answers: int
    total_time: int
    performance_trend: List[float]
    adaptive_parameters: Dict[str, Any]

class AdaptiveQuizEngine:
    """Main adaptive quiz engine with AI integration"""
    
    def __init__(self, educational_assistant: EducationalAssistant):
        self.ai_assistant = educational_assistant
        self.question_bank = self._initialize_question_bank()
        self.difficulty_thresholds = {
            'promote': 0.8,  # 80% accuracy to increase difficulty
            'demote': 0.4,   # Below 40% accuracy to decrease difficulty
            'maintain': 0.6  # 60% accuracy to maintain difficulty
        }
        
    def _initialize_question_bank(self) -> Dict[str, List[QuizQuestion]]:
        """Initialize question bank with sample questions"""
        return {
            "Python Programming": [
                QuizQuestion(
                    question_id="py_001",
                    subject="Python Programming",
                    topic="Variables and Data Types",
                    question_text="What is the output of: print(type(5.0))?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    difficulty_level=DifficultyLevel.BEGINNER,
                    options=["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>"],
                    correct_answer="<class 'float'>",
                    explanation="5.0 is a floating-point number, so type(5.0) returns <class 'float'>",
                    hints=["Look at the decimal point", "Python distinguishes between integers and floats"],
                    estimated_time=30,
                    tags=["data_types", "built_in_functions"],
                    metadata={"concept": "type_system"}
                ),
                QuizQuestion(
                    question_id="py_002",
                    subject="Python Programming",
                    topic="Control Flow",
                    question_text="Complete the code: for i in _____(5): print(i)",
                    question_type=QuestionType.FILL_BLANK,
                    difficulty_level=DifficultyLevel.BEGINNER,
                    options=[],
                    correct_answer="range",
                    explanation="The range() function generates a sequence of numbers from 0 to n-1",
                    hints=["Think about generating sequences", "It's a built-in function"],
                    estimated_time=45,
                    tags=["loops", "range_function"],
                    metadata={"concept": "iteration"}
                ),
                QuizQuestion(
                    question_id="py_003",
                    subject="Python Programming",
                    topic="Functions",
                    question_text="What will this function return?\n\ndef mystery(x, y=10):\n    return x * y\n\nresult = mystery(5)",
                    question_type=QuestionType.SHORT_ANSWER,
                    difficulty_level=DifficultyLevel.INTERMEDIATE,
                    options=[],
                    correct_answer="50",
                    explanation="The function multiplies x (5) by y (default value 10), resulting in 50",
                    hints=["Check the default parameter value", "What happens when y is not provided?"],
                    estimated_time=60,
                    tags=["functions", "default_parameters"],
                    metadata={"concept": "function_parameters"}
                )
            ],
            "Mathematics": [
                QuizQuestion(
                    question_id="math_001",
                    subject="Mathematics",
                    topic="Algebra",
                    question_text="Solve for x: 2x + 5 = 15",
                    question_type=QuestionType.SHORT_ANSWER,
                    difficulty_level=DifficultyLevel.BEGINNER,
                    options=[],
                    correct_answer="5",
                    explanation="Subtract 5 from both sides: 2x = 10, then divide by 2: x = 5",
                    hints=["Isolate the variable", "Use inverse operations"],
                    estimated_time=90,
                    tags=["linear_equations", "algebra"],
                    metadata={"concept": "equation_solving"}
                )
            ]
        }
    
    def start_quiz_session(self, user_id: str, subject: str, 
                          initial_difficulty: DifficultyLevel = DifficultyLevel.BEGINNER) -> str:
        """Start a new adaptive quiz session"""
        session_id = f"quiz_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = QuizSession(
            session_id=session_id,
            user_id=user_id,
            subject=subject,
            start_time=datetime.now(),
            current_difficulty=initial_difficulty,
            questions_answered=0,
            correct_answers=0,
            total_time=0,
            performance_trend=[],
            adaptive_parameters={
                'consecutive_correct': 0,
                'consecutive_incorrect': 0,
                'time_pressure_factor': 1.0,
                'confidence_trend': []
            }
        )
        
        # Store session in Streamlit session state
        if 'quiz_sessions' not in st.session_state:
            st.session_state.quiz_sessions = {}
        st.session_state.quiz_sessions[session_id] = session
        
        return session_id
    
    def get_next_question(self, session_id: str) -> Optional[QuizQuestion]:
        """Get the next adaptive question based on performance"""
        if session_id not in st.session_state.quiz_sessions:
            return None
            
        session = st.session_state.quiz_sessions[session_id]
        
        # Get available questions for current difficulty and subject
        available_questions = self._get_questions_by_criteria(
            subject=session.subject,
            difficulty=session.current_difficulty,
            exclude_answered=self._get_answered_questions(session_id)
        )
        
        if not available_questions:
            # Generate new question using AI if none available
            return self._generate_ai_question(session)
        
        # Select question based on adaptive algorithm
        selected_question = self._select_adaptive_question(available_questions, session)
        return selected_question
    
    def submit_answer(self, session_id: str, question_id: str, user_answer: str,
                     time_taken: int, confidence_level: int = 3,
                     hints_used: int = 0) -> Dict[str, Any]:
        """Submit answer and get immediate feedback with difficulty adjustment"""
        if session_id not in st.session_state.quiz_sessions:
            return {"error": "Session not found"}
        
        session = st.session_state.quiz_sessions[session_id]
        question = self._get_question_by_id(question_id)
        
        if not question:
            return {"error": "Question not found"}
        
        # Evaluate answer
        is_correct = self._evaluate_answer(question, user_answer)
        
        # Create attempt record
        attempt = QuizAttempt(
            attempt_id=f"attempt_{session_id}_{question_id}",
            user_id=session.user_id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_taken=time_taken,
            hints_used=hints_used,
            difficulty_at_attempt=session.current_difficulty,
            timestamp=datetime.now(),
            confidence_level=confidence_level
        )
        
        # Store attempt
        if 'quiz_attempts' not in st.session_state:
            st.session_state.quiz_attempts = []
        st.session_state.quiz_attempts.append(attempt)
        
        # Update session statistics
        session.questions_answered += 1
        session.total_time += time_taken
        if is_correct:
            session.correct_answers += 1
            session.adaptive_parameters['consecutive_correct'] += 1
            session.adaptive_parameters['consecutive_incorrect'] = 0
        else:
            session.adaptive_parameters['consecutive_correct'] = 0
            session.adaptive_parameters['consecutive_incorrect'] += 1
        
        # Calculate current performance
        current_accuracy = session.correct_answers / session.questions_answered
        session.performance_trend.append(current_accuracy)
        session.adaptive_parameters['confidence_trend'].append(confidence_level)
        
        # Adjust difficulty
        new_difficulty = self._adjust_difficulty(session, attempt)
        session.current_difficulty = new_difficulty
        
        # Generate AI feedback
        feedback = self._generate_ai_feedback(question, attempt, session)
        
        # Prepare response
        response = {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "ai_feedback": feedback,
            "current_accuracy": current_accuracy,
            "difficulty_adjusted": new_difficulty != question.difficulty_level,
            "new_difficulty": new_difficulty.name,
            "performance_trend": session.performance_trend[-5:],  # Last 5 questions
            "session_stats": {
                "questions_answered": session.questions_answered,
                "correct_answers": session.correct_answers,
                "total_time": session.total_time,
                "average_time": session.total_time / session.questions_answered
            }
        }
        
        return response
    
    def _get_questions_by_criteria(self, subject: str, difficulty: DifficultyLevel,
                                 exclude_answered: List[str]) -> List[QuizQuestion]:
        """Get questions matching criteria"""
        if subject not in self.question_bank:
            return []
        
        questions = [
            q for q in self.question_bank[subject]
            if q.difficulty_level == difficulty and q.question_id not in exclude_answered
        ]
        
        return questions
    
    def _get_answered_questions(self, session_id: str) -> List[str]:
        """Get list of already answered question IDs"""
        if 'quiz_attempts' not in st.session_state:
            return []
        
        session = st.session_state.quiz_sessions[session_id]
        answered = [
            attempt.question_id for attempt in st.session_state.quiz_attempts
            if attempt.user_id == session.user_id
        ]
        
        return answered
    
    def _select_adaptive_question(self, questions: List[QuizQuestion], 
                                session: QuizSession) -> QuizQuestion:
        """Select question using adaptive algorithm"""
        if not questions:
            return None
        
        # Weight questions based on performance trends
        weights = []
        for question in questions:
            weight = 1.0
            
            # Prefer topics where user struggled recently
            if session.performance_trend:
                recent_performance = sum(session.performance_trend[-3:]) / len(session.performance_trend[-3:])
                if recent_performance < 0.6:
                    weight *= 1.5  # Increase weight for review
            
            # Consider time pressure
            time_factor = session.adaptive_parameters.get('time_pressure_factor', 1.0)
            if time_factor > 1.2:  # User is taking too long
                if question.estimated_time < 60:  # Prefer shorter questions
                    weight *= 1.3
            
            weights.append(weight)
        
        # Select question using weighted random choice
        selected_question = random.choices(questions, weights=weights)[0]
        return selected_question
    
    def _evaluate_answer(self, question: QuizQuestion, user_answer: str) -> bool:
        """Evaluate if the user's answer is correct"""
        user_answer = user_answer.strip().lower()
        correct_answer = question.correct_answer.strip().lower()
        
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            return user_answer == correct_answer
        elif question.question_type == QuestionType.TRUE_FALSE:
            return user_answer in ['true', 't', 'yes', 'y'] and correct_answer in ['true', 't', 'yes', 'y'] or \
                   user_answer in ['false', 'f', 'no', 'n'] and correct_answer in ['false', 'f', 'no', 'n']
        elif question.question_type == QuestionType.SHORT_ANSWER:
            # Allow for minor variations in numeric answers
            try:
                return abs(float(user_answer) - float(correct_answer)) < 0.01
            except ValueError:
                return user_answer == correct_answer
        elif question.question_type == QuestionType.FILL_BLANK:
            return user_answer == correct_answer
        else:
            return user_answer == correct_answer
    
    def _adjust_difficulty(self, session: QuizSession, attempt: QuizAttempt) -> DifficultyLevel:
        """Adjust difficulty based on performance"""
        current_accuracy = session.correct_answers / session.questions_answered
        consecutive_correct = session.adaptive_parameters['consecutive_correct']
        consecutive_incorrect = session.adaptive_parameters['consecutive_incorrect']
        
        current_difficulty = session.current_difficulty
        
        # Promote difficulty
        if (current_accuracy >= self.difficulty_thresholds['promote'] and 
            consecutive_correct >= 3 and 
            current_difficulty != DifficultyLevel.EXPERT):
            return DifficultyLevel(current_difficulty.value + 1)
        
        # Demote difficulty
        elif (current_accuracy <= self.difficulty_thresholds['demote'] and 
              consecutive_incorrect >= 2 and 
              current_difficulty != DifficultyLevel.BEGINNER):
            return DifficultyLevel(current_difficulty.value - 1)
        
        # Maintain current difficulty
        return current_difficulty
    
    def _generate_ai_feedback(self, question: QuizQuestion, attempt: QuizAttempt,
                            session: QuizSession) -> str:
        """Generate personalized AI feedback"""
        try:
            prompt = f"""
            Generate personalized feedback for a student's quiz attempt:
            
            Question: {question.question_text}
            Correct Answer: {question.correct_answer}
            Student Answer: {attempt.user_answer}
            Is Correct: {attempt.is_correct}
            Difficulty Level: {question.difficulty_level.name}
            Time Taken: {attempt.time_taken} seconds
            Student's Current Accuracy: {session.correct_answers / session.questions_answered:.2%}
            
            Provide:
            1. Encouraging feedback (2-3 sentences)
            2. Specific explanation of why the answer is right/wrong
            3. A helpful tip for similar questions
            4. Next steps recommendation
            
            Keep it concise, encouraging, and educational.
            """
            
            # Create a temporary user profile for the AI assistant
            temp_profile = {
                'name': 'Student',
                'learning_style': 'Visual',
                'subjects': [session.subject],
                'difficulty_level': session.current_difficulty.name
            }
            
            response = self.ai_assistant.generate_response(prompt, temp_profile)
            return response
            
        except Exception as e:
            # Fallback feedback
            if attempt.is_correct:
                return f"Great job! You correctly answered this {question.difficulty_level.name.lower()} level question. {question.explanation}"
            else:
                return f"Not quite right. {question.explanation} Keep practicing - you're making good progress!"
    
    def _generate_ai_question(self, session: QuizSession) -> Optional[QuizQuestion]:
        """Generate a new question using AI when question bank is exhausted"""
        try:
            prompt = f"""
            Generate a {session.current_difficulty.name.lower()} level quiz question for {session.subject}.
            
            Format as JSON:
            {{
                "question_text": "The question text",
                "question_type": "multiple_choice|true_false|short_answer|fill_blank",
                "options": ["option1", "option2", "option3", "option4"],
                "correct_answer": "correct answer",
                "explanation": "why this is correct",
                "topic": "specific topic name",
                "estimated_time": 60
            }}
            
            Make it educational and appropriate for the difficulty level.
            """
            
            # Create a temporary user profile for the AI assistant
            temp_profile = {
                'name': 'Student',
                'learning_style': 'Visual',
                'subjects': [session.subject],
                'difficulty_level': session.current_difficulty.name
            }
            
            response = self.ai_assistant.generate_response(prompt, temp_profile)
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    question_data = json.loads(json_match.group())
                else:
                    # If no JSON found, return None to use fallback
                    return None
            except (json.JSONDecodeError, AttributeError):
                return None
            
            # Create QuizQuestion object
            question = QuizQuestion(
                question_id=f"ai_gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                subject=session.subject,
                topic=question_data.get('topic', 'General'),
                question_text=question_data['question_text'],
                question_type=QuestionType(question_data['question_type']),
                difficulty_level=session.current_difficulty,
                options=question_data.get('options', []),
                correct_answer=question_data['correct_answer'],
                explanation=question_data['explanation'],
                hints=[],
                estimated_time=question_data.get('estimated_time', 60),
                tags=['ai_generated'],
                metadata={'generated_at': datetime.now().isoformat()}
            )
            
            return question
            
        except Exception as e:
            st.error(f"Failed to generate AI question: {e}")
            return None
    
    def _get_question_by_id(self, question_id: str) -> Optional[QuizQuestion]:
        """Get question by ID from question bank"""
        for subject_questions in self.question_bank.values():
            for question in subject_questions:
                if question.question_id == question_id:
                    return question
        return None
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        if session_id not in st.session_state.quiz_sessions:
            return {}
        
        session = st.session_state.quiz_sessions[session_id]
        attempts = [
            attempt for attempt in st.session_state.get('quiz_attempts', [])
            if attempt.user_id == session.user_id
        ]
        
        if not attempts:
            return {}
        
        # Calculate detailed statistics
        total_time = sum(attempt.time_taken for attempt in attempts)
        avg_time = total_time / len(attempts) if attempts else 0
        accuracy = session.correct_answers / session.questions_answered if session.questions_answered > 0 else 0
        
        # Performance by difficulty
        difficulty_stats = {}
        for attempt in attempts:
            diff_name = attempt.difficulty_at_attempt.name
            if diff_name not in difficulty_stats:
                difficulty_stats[diff_name] = {'correct': 0, 'total': 0}
            difficulty_stats[diff_name]['total'] += 1
            if attempt.is_correct:
                difficulty_stats[diff_name]['correct'] += 1
        
        return {
            'session_id': session_id,
            'subject': session.subject,
            'duration': (datetime.now() - session.start_time).total_seconds() / 60,
            'questions_answered': session.questions_answered,
            'correct_answers': session.correct_answers,
            'accuracy': accuracy,
            'average_time_per_question': avg_time,
            'final_difficulty': session.current_difficulty.name,
            'performance_trend': session.performance_trend,
            'difficulty_breakdown': difficulty_stats,
            'total_time_spent': total_time
        }

class QuizInterface:
    """Streamlit interface for the adaptive quiz system"""
    
    def __init__(self, quiz_engine: AdaptiveQuizEngine):
        self.quiz_engine = quiz_engine
    
    def render_quiz_interface(self, user_id: str):
        """Render the main quiz interface"""
        st.header("🧠 Adaptive Quiz System")
        
        # Initialize session state
        if 'current_quiz_session' not in st.session_state:
            st.session_state.current_quiz_session = None
        if 'current_question' not in st.session_state:
            st.session_state.current_question = None
        if 'quiz_start_time' not in st.session_state:
            st.session_state.quiz_start_time = None
        
        # Quiz setup or continue
        if not st.session_state.current_quiz_session:
            self._render_quiz_setup(user_id)
        else:
            self._render_active_quiz(user_id)
    
    def _render_quiz_setup(self, user_id: str):
        """Render quiz setup interface"""
        st.subheader("Start New Quiz")
        
        # Subject selection
        subjects = list(self.quiz_engine.question_bank.keys())
        subject = st.selectbox("Select Subject", subjects)
        
        # Difficulty selection
        difficulty_options = {
            "Beginner": DifficultyLevel.BEGINNER,
            "Intermediate": DifficultyLevel.INTERMEDIATE,
            "Advanced": DifficultyLevel.ADVANCED,
            "Expert": DifficultyLevel.EXPERT
        }
        
        difficulty_choice = st.radio(
            "Select Starting Difficulty",
            options=list(difficulty_options.keys()),
            horizontal=True
        )
        
        # Start button
        if st.button("Start Quiz", type="primary"):
            # Create new session
            session_id = self.quiz_engine.start_quiz_session(
                user_id=user_id,
                subject=subject,
                initial_difficulty=difficulty_options[difficulty_choice]
            )
            
            # Initialize session state
            if 'quiz_sessions' not in st.session_state:
                st.session_state.quiz_sessions = {}
                
            # Store session
            st.session_state.current_quiz_session = session_id
            # Session is already stored in st.session_state.quiz_sessions by start_quiz_session method
            st.session_state.current_question = None
            
            st.success(f"Starting new {subject} quiz at {difficulty_choice} level!")
            st.rerun()
            
    def _render_active_quiz(self, user_id: str):
        """Render active quiz interface"""
        session_id = st.session_state.current_quiz_session
        session = st.session_state.quiz_sessions[session_id]
        
        # Quiz header with progress
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(f"📚 {session.subject} Quiz")
        
        with col2:
            accuracy = session.correct_answers / max(session.questions_answered, 1)
            st.metric("Accuracy", f"{accuracy:.1%}")
        
        with col3:
            st.metric("Questions", f"{session.questions_answered}")
        
        # Current difficulty indicator
        difficulty_colors = {
            DifficultyLevel.BEGINNER: "🟢",
            DifficultyLevel.INTERMEDIATE: "🟡", 
            DifficultyLevel.ADVANCED: "🟠",
            DifficultyLevel.EXPERT: "🔴"
        }
        
        # Safe access to difficulty colors with fallback
        difficulty_icon = difficulty_colors.get(session.current_difficulty, "⚪")
        difficulty_name = session.current_difficulty.name.title() if hasattr(session.current_difficulty, 'name') else str(session.current_difficulty)
        st.info(f"Current Difficulty: {difficulty_icon} {difficulty_name}")
        
        # Get or display current question
        if not st.session_state.current_question:
            question = self.quiz_engine.get_next_question(session_id)
            if question:
                st.session_state.current_question = question
                st.session_state.quiz_start_time = datetime.now()
            else:
                st.success("🎉 Quiz completed! No more questions available.")
                self._render_quiz_summary(session_id)
                return
        
        question = st.session_state.current_question
        
        # Display question
        st.markdown("---")
        st.markdown(f"**Question {session.questions_answered + 1}:**")
        st.markdown(question.question_text)
        
        # Question type specific input
        user_answer = self._render_question_input(question)
        
        # Confidence level
        confidence = st.slider(
            "How confident are you in your answer?",
            min_value=1, max_value=5, value=3,
            help="1 = Not confident, 5 = Very confident"
        )
        
        # Submit answer
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("Submit Answer", type="primary"):
                if user_answer:
                    self._submit_answer(session_id, question, user_answer, confidence)
                else:
                    st.error("Please provide an answer before submitting.")
        
        with col2:
            if st.button("Skip Question"):
                st.session_state.current_question = None
                st.rerun()
        
        with col3:
            if st.button("End Quiz"):
                self._end_quiz(session_id)
                
    def _render_question_input(self, question: QuizQuestion) -> str:
        """Render input based on question type"""
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            return st.radio("Select your answer:", question.options, key="quiz_answer")
        
        elif question.question_type == QuestionType.TRUE_FALSE:
            return st.radio("Select your answer:", ["True", "False"], key="quiz_answer")
        
        elif question.question_type == QuestionType.SHORT_ANSWER:
            return st.text_input("Your answer:", key="quiz_answer")
        
        elif question.question_type == QuestionType.FILL_BLANK:
            return st.text_input("Fill in the blank:", key="quiz_answer")
        
        elif question.question_type == QuestionType.CODE_COMPLETION:
            return st.text_area("Complete the code:", height=100, key="quiz_answer")
        
        else:
            return st.text_input("Your answer:", key="quiz_answer")
            
    def _submit_answer(self, session_id: str, question: QuizQuestion, 
                      user_answer: str, confidence: int):
        """Submit answer and show feedback"""
        time_taken = int((datetime.now() - st.session_state.quiz_start_time).total_seconds())
        
        result = self.quiz_engine.submit_answer(
            session_id, question.question_id, user_answer, 
            time_taken, confidence
        )
        
        # Show immediate feedback
        if result['is_correct']:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect")
            st.info(f"**Correct Answer:** {result['correct_answer']}")
        
        st.markdown(f"**Explanation:** {result['explanation']}")
        
        if result['ai_feedback']:
            st.markdown(f"**AI Tutor:** {result['ai_feedback']}")
        
        # Show performance update
        if result['difficulty_adjusted']:
            if result['new_difficulty'] == 'EXPERT':
                st.balloons()
                st.success(f"🎯 Difficulty increased to {result['new_difficulty']}! You're doing great!")
            elif result['new_difficulty'] == 'BEGINNER':
                st.info(f"📚 Difficulty adjusted to {result['new_difficulty']} to help you learn better.")
            else:
                st.info(f"⚡ Difficulty adjusted to {result['new_difficulty']}")
        
        # Continue button
        if st.button("Next Question", type="primary"):
            st.session_state.current_question = None
            st.rerun()
            
    def _render_quiz_summary(self, session_id: str):
        """Render quiz completion summary"""
        summary = self.quiz_engine.get_session_summary(session_id)
        
        if not summary:
            return
        
        st.header("📊 Quiz Summary")
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Questions Answered", summary['questions_answered'])
        
        with col2:
            st.metric("Accuracy", f"{summary['accuracy']:.1%}")
        
        with col3:
            st.metric("Avg Time/Question", f"{summary['average_time_per_question']:.1f}s")
        
        with col4:
            st.metric("Final Difficulty", summary['final_difficulty'])
        
        # Performance chart
        if summary['performance_trend']:
            st.subheader("Performance Trend")
            st.line_chart(summary['performance_trend'])
        
        # Difficulty breakdown
        if summary['difficulty_breakdown']:
            st.subheader("Performance by Difficulty")
            for difficulty, stats in summary['difficulty_breakdown'].items():
                accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
                st.write(f"**{difficulty}:** {stats['correct']}/{stats['total']} ({accuracy:.1%})")
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Start New Quiz"):
                st.session_state.current_quiz_session = None
                st.session_state.current_question = None
                st.rerun()
        
        with col2:
            if st.button("View Detailed Analytics"):
                st.info("Detailed analytics would be shown here in a full implementation.")
    
    def _end_quiz(self, session_id: str):
        """End the current quiz session"""
        st.session_state.current_quiz_session = None
        st.session_state.current_question = None
        st.success("Quiz ended. Thank you for practicing!")
        st.rerun()

class AdaptiveQuizInterface:
    """Streamlit interface wrapper for the adaptive quiz system"""
    
    def __init__(self, educational_assistant):
        self.quiz_engine = AdaptiveQuizEngine(educational_assistant)
        self.quiz_interface = QuizInterface(self.quiz_engine)
    
    def render_interface(self):
        """Render the adaptive quiz interface"""
        if 'user_profile' in st.session_state and st.session_state.user_profile:
            user_id = st.session_state.user_profile.get('name', 'user')
            self.quiz_interface.render_quiz_interface(user_id)
        else:
            st.warning("Please complete your profile setup first.")