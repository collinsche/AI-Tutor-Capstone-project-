#!/usr/bin/env python3
"""
Utility Functions
Helper functions for the AI Educational Assistant
"""

import os
import re
import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)
    
    # Limit length
    return sanitized[:1000]


def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return timestamp


def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Calculate estimated reading time in minutes"""
    word_count = len(text.split())
    return max(1, word_count // words_per_minute)


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text"""
    if not text:
        return []
    
    # Simple keyword extraction
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Count word frequency
    word_freq: Dict[str, int] = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get most frequent words
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Filter out common words
    common_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 
        'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 
        'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'
    }
    
    keywords = [word for word, _ in sorted_words if word not in common_words]
    return keywords[:max_keywords]


def generate_session_id() -> str:
    """Generate a unique session ID"""
    timestamp = datetime.now().isoformat()
    return hashlib.md5(timestamp.encode()).hexdigest()[:12]


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_duration(seconds: int) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts (simple implementation)"""
    if not text1 or not text2:
        return 0.0
    
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at word boundary
        if end < len(text):
            last_space = chunk.rfind(' ')
            if last_space > chunk_size // 2:
                chunk = chunk[:last_space]
                end = start + last_space
        
        chunks.append(chunk)
        start = end - overlap
        
        if start >= len(text):
            break
    
    return chunks


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON with fallback"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """Safely dump JSON with fallback"""
    try:
        return json.dumps(obj, indent=2)
    except (TypeError, ValueError):
        return default


def get_file_size(file_path: str) -> str:
    """Get human-readable file size"""
    try:
        size_bytes = os.path.getsize(file_path)
        
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes/(1024 ** 2):.1f} MB"
        else:
            return f"{size_bytes/(1024 ** 3):.1f} GB"
    except OSError:
        return "Unknown"


def create_progress_bar(current: int, total: int, width: int = 20) -> str:
    """Create a text-based progress bar"""
    if total == 0:
        return "█" * width
    
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(progress * 100)
    
    return f"{bar} {percentage}%"


def validate_learning_style(style: str) -> bool:
    """Validate learning style"""
    valid_styles = ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"]
    return style in valid_styles


def get_difficulty_color(difficulty: str) -> str:
    """Get color for difficulty level"""
    colors = {
        "Beginner": "#4CAF50",
        "Intermediate": "#FF9800", 
        "Advanced": "#F44336"
    }
    return colors.get(difficulty, "#9E9E9E")


def format_learning_time(minutes: float) -> str:
    """Format learning time"""
    if minutes < 60:
        return f"{int(minutes)} min"
    else:
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return f"{hours}h {mins}m"


def generate_study_schedule(subjects: List[str], available_hours: int = 2) -> Dict[str, int]:
    """Generate a study schedule"""
    if not subjects:
        return {}
    
    minutes_per_subject = (available_hours * 60) // len(subjects)
    schedule = {}
    
    for subject in subjects:
        schedule[subject] = minutes_per_subject
    
    return schedule


def calculate_learning_streak(sessions: List[Dict]) -> int:
    """Calculate current learning streak"""
    if not sessions:
        return 0
    
    # Sort sessions by date
    sorted_sessions = sorted(sessions, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    streak = 0
    current_date = datetime.now().date()
    
    for session in sorted_sessions:
        try:
            session_date = datetime.fromisoformat(session.get('timestamp', '')).date()
            
            # Check if session is from today or consecutive days
            if session_date == current_date or (current_date - session_date).days == streak + 1:
                streak += 1
                current_date = session_date
            else:
                break
        except (ValueError, TypeError):
            continue
    
    return streak


def get_motivational_message(streak: int, progress: float) -> str:
    """Get motivational message based on streak and progress"""
    messages = {
        0: "Start your learning journey today! 🚀",
        1: "Great start! Keep the momentum going! 💪",
        3: "You're on fire! 3 days in a row! 🔥",
        7: "Amazing! A full week of learning! 🌟",
        14: "Incredible! Two weeks of dedication! 🏆",
        30: "Outstanding! A month of consistent learning! 🎉"
    }
    
    # Find the appropriate message
    for threshold in sorted(messages.keys(), reverse=True):
        if streak >= threshold:
            return messages[threshold]
    
    return "Keep learning and growing! 📚"


def streamlit_style_metric(label: str, value: str, delta: Optional[str] = None) -> None:
    """Create a styled metric display"""
    st.metric(label=label, value=value, delta=delta)


def create_learning_badge(achievement: str) -> str:
    """Create a learning achievement badge"""
    badges = {
        "first_session": "🎯 First Steps",
        "week_streak": "🔥 Week Warrior",
        "month_streak": "💎 Monthly Master",
        "quiz_master": "🧠 Quiz Master",
        "fast_learner": "⚡ Speed Learner"
    }
    
    return badges.get(achievement, "🏅 Achievement")


def log_user_action(action: str, details: Dict[str, Any] = None):
    """Log user action for analytics"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details or {}
    }
    
    logger.info(f"User action: {json.dumps(log_entry)}")


def handle_error(error: Exception, context: str = "") -> str:
    """Handle and log errors gracefully"""
    error_msg = f"Error in {context}: {str(error)}" if context else str(error)
    logger.error(error_msg)
    
    # Return user-friendly message
    return "I encountered an issue while processing your request. Please try again."