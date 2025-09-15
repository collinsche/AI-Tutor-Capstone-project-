#!/usr/bin/env python3
"""
Utility Functions
Helper functions for the AI Educational Assistant
"""

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
    if not isinstance(text, str):
        return ""
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\'\/\\]', '', text)
    
    # Limit length
    sanitized = sanitized[:1000]
    
    # Strip whitespace
    sanitized = sanitized.strip()
    
    return sanitized

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp

def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Calculate estimated reading time in minutes"""
    word_count = len(text.split())
    reading_time = max(1, word_count // words_per_minute)
    return reading_time

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text using simple frequency analysis"""
    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those'
    }
    
    # Filter words and count frequency
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    word_freq = {}
    for word in filtered_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:max_keywords]]

def generate_session_id() -> str:
    """Generate a unique session ID"""
    timestamp = datetime.now().isoformat()
    hash_input = f"{timestamp}_{id(object())}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:12]

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity using Jaccard similarity"""
    if not text1 or not text2:
        return 0.0
    
    # Convert to sets of words
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0

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
            if last_space > chunk_size * 0.8:  # Only if we don't lose too much
                chunk = chunk[:last_space]
                end = start + last_space
        
        chunks.append(chunk.strip())
        start = end - overlap
        
        if start >= len(text):
            break
    
    return chunks

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string with fallback"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """Safely dump object to JSON string with fallback"""
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except (TypeError, ValueError):
        return default

def get_file_size(file_path: str) -> str:
    """Get human-readable file size"""
    try:
        size_bytes = os.path.getsize(file_path)
        
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    except OSError:
        return "Unknown"

def create_progress_bar(current: int, total: int, width: int = 20) -> str:
    """Create a text-based progress bar"""
    if total == 0:
        return "[" + " " * width + "] 0%"
    
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(progress * 100)
    
    return f"[{bar}] {percentage}%"

def validate_learning_style(style: str) -> bool:
    """Validate learning style"""
    valid_styles = ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"]
    return style in valid_styles

def get_difficulty_color(difficulty: str) -> str:
    """Get color code for difficulty level"""
    colors = {
        "Beginner": "#28a745",  # Green
        "Intermediate": "#ffc107",  # Yellow
        "Advanced": "#dc3545"  # Red
    }
    return colors.get(difficulty, "#6c757d")  # Default gray

def format_learning_time(minutes: float) -> str:
    """Format learning time for display"""
    if minutes < 1:
        return "< 1 min"
    elif minutes < 60:
        return f"{int(minutes)} min"
    else:
        hours = minutes / 60
        return f"{hours:.1f} hrs"

def generate_study_schedule(subjects: List[str], available_hours: int = 2) -> Dict[str, int]:
    """Generate a simple study schedule"""
    if not subjects:
        return {}
    
    # Distribute time evenly among subjects
    time_per_subject = available_hours * 60 // len(subjects)  # in minutes
    
    schedule = {}
    for subject in subjects:
        schedule[subject] = time_per_subject
    
    return schedule

def calculate_learning_streak(sessions: List[Dict]) -> int:
    """Calculate current learning streak in days"""
    if not sessions:
        return 0
    
    # Sort sessions by date
    sorted_sessions = sorted(sessions, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    streak = 0
    current_date = datetime.now().date()
    
    for session in sorted_sessions:
        try:
            session_date = datetime.fromisoformat(session['timestamp']).date()
            
            if session_date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif session_date == current_date + timedelta(days=1):
                # Continue streak
                current_date = session_date - timedelta(days=1)
            else:
                # Streak broken
                break
        except:
            continue
    
    return streak

def get_motivational_message(streak: int, progress: float) -> str:
    """Get motivational message based on progress"""
    messages = {
        "high_streak": [
            "🔥 You're on fire! Keep up the amazing streak!",
            "⭐ Consistency is key to success - you're nailing it!",
            "🚀 Your dedication is inspiring!"
        ],
        "good_progress": [
            "📈 Great progress! You're moving in the right direction!",
            "💪 Keep pushing forward - you're doing great!",
            "🎯 You're building excellent learning habits!"
        ],
        "encouragement": [
            "🌱 Every expert was once a beginner - keep growing!",
            "📚 Learning is a journey, not a destination!",
            "✨ Small steps lead to big achievements!"
        ]
    }
    
    if streak >= 7:
        return messages["high_streak"][streak % len(messages["high_streak"])]
    elif progress > 0.7:
        return messages["good_progress"][int(progress * 10) % len(messages["good_progress"])]
    else:
        return messages["encouragement"][streak % len(messages["encouragement"])]

def streamlit_style_metric(label: str, value: str, delta: Optional[str] = None) -> None:
    """Create a styled metric display for Streamlit"""
    if delta:
        st.metric(label=label, value=value, delta=delta)
    else:
        st.metric(label=label, value=value)

def create_learning_badge(achievement: str) -> str:
    """Create HTML for learning achievement badge"""
    badges = {
        "first_session": "🎓 First Steps",
        "week_streak": "🔥 Week Warrior",
        "month_streak": "💎 Monthly Master",
        "subject_expert": "🏆 Subject Expert",
        "quick_learner": "⚡ Quick Learner",
        "persistent": "🎯 Persistent Learner"
    }
    
    badge_text = badges.get(achievement, "🌟 Achievement")
    
    return f"""
    <div style="
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        display: inline-block;
        margin: 2px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        {badge_text}
    </div>
    """

def log_user_action(action: str, details: Dict[str, Any] = None):
    """Log user action for analytics"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details or {}
    }
    
    logger.info(f"User action: {action}", extra=log_entry)

def handle_error(error: Exception, context: str = "") -> str:
    """Handle and format errors for user display"""
    error_message = f"An error occurred: {str(error)}"
    
    if context:
        error_message = f"{context}: {error_message}"
    
    logger.error(error_message, exc_info=True)
    
    # Return user-friendly message
    return "I encountered an issue while processing your request. Please try again."