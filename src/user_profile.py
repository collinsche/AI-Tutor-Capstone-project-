#!/usr/bin/env python3
"""
User Profile Module
Handles user data and personalization settings
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class UserProfile:
    """User profile management class"""
    
    def __init__(self, profile_file: str = "user_profile.json"):
        """Initialize user profile"""
        self.profile_file = profile_file
        self.name = ""
        self.learning_style = "Visual"  # Default learning style
        self.subjects = []
        self.preferences = {}
        self.learning_history = []
        self.created_at = datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()
        
        # Load existing profile if available
        self.load_profile()
    
    def update_profile(self, name: str, learning_style: str, subjects: List[str], 
                      preferences: Optional[Dict] = None):
        """Update user profile information"""
        self.name = name
        self.learning_style = learning_style
        self.subjects = subjects
        if preferences:
            self.preferences.update(preferences)
        self.last_updated = datetime.now().isoformat()
        
        # Save updated profile
        self.save_profile()
    
    def add_learning_session(self, session_data: Dict[str, Any]):
        """Add a learning session to history"""
        session = {
            "timestamp": datetime.now().isoformat(),
            "duration": session_data.get("duration", 0),
            "topics_covered": session_data.get("topics", []),
            "questions_asked": session_data.get("questions", 0),
            "difficulty_level": session_data.get("difficulty", "medium"),
            "satisfaction_score": session_data.get("satisfaction", None)
        }
        
        self.learning_history.append(session)
        self.last_updated = datetime.now().isoformat()
        self.save_profile()
    
    def get_learning_preferences(self) -> Dict[str, Any]:
        """Get learning preferences based on profile and history"""
        preferences = {
            "learning_style": self.learning_style,
            "preferred_subjects": self.subjects,
            "difficulty_preference": self._analyze_difficulty_preference(),
            "session_length_preference": self._analyze_session_length(),
            "best_learning_times": self._analyze_learning_patterns(),
            "content_format": self._get_content_format_preference()
        }
        
        return preferences
    
    def _analyze_difficulty_preference(self) -> str:
        """Analyze preferred difficulty level from history"""
        if not self.learning_history:
            return "medium"
        
        difficulty_counts = {"easy": 0, "medium": 0, "hard": 0}
        satisfaction_by_difficulty = {"easy": [], "medium": [], "hard": []}
        
        for session in self.learning_history:
            difficulty = session.get("difficulty_level", "medium")
            satisfaction = session.get("satisfaction_score")
            
            if difficulty in difficulty_counts:
                difficulty_counts[difficulty] += 1
                if satisfaction is not None:
                    satisfaction_by_difficulty[difficulty].append(satisfaction)
        
        # Find difficulty with highest average satisfaction
        best_difficulty = "medium"
        best_avg_satisfaction = 0
        
        for difficulty, scores in satisfaction_by_difficulty.items():
            if scores:
                avg_satisfaction = sum(scores) / len(scores)
                if avg_satisfaction > best_avg_satisfaction:
                    best_avg_satisfaction = avg_satisfaction
                    best_difficulty = difficulty
        
        return best_difficulty
    
    def _analyze_session_length(self) -> int:
        """Analyze preferred session length in minutes"""
        if not self.learning_history:
            return 30  # Default 30 minutes
        
        durations = [session.get("duration", 30) for session in self.learning_history]
        avg_duration = sum(durations) / len(durations)
        
        return int(avg_duration)
    
    def _analyze_learning_patterns(self) -> List[str]:
        """Analyze learning time patterns"""
        if not self.learning_history:
            return ["morning", "afternoon"]
        
        # Simple pattern analysis based on timestamps
        time_patterns = {"morning": 0, "afternoon": 0, "evening": 0}
        
        for session in self.learning_history:
            timestamp = session.get("timestamp", "")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hour = dt.hour
                    
                    if 6 <= hour < 12:
                        time_patterns["morning"] += 1
                    elif 12 <= hour < 18:
                        time_patterns["afternoon"] += 1
                    else:
                        time_patterns["evening"] += 1
                except:
                    continue
        
        # Return top 2 preferred times
        sorted_times = sorted(time_patterns.items(), key=lambda x: x[1], reverse=True)
        return [time for time, count in sorted_times[:2] if count > 0]
    
    def _get_content_format_preference(self) -> Dict[str, str]:
        """Get content format preferences based on learning style"""
        format_preferences = {
            "Visual": {
                "primary": "diagrams_and_charts",
                "secondary": "videos",
                "avoid": "long_text_blocks"
            },
            "Auditory": {
                "primary": "audio_explanations",
                "secondary": "discussions",
                "avoid": "silent_reading"
            },
            "Kinesthetic": {
                "primary": "interactive_exercises",
                "secondary": "simulations",
                "avoid": "passive_content"
            },
            "Reading/Writing": {
                "primary": "detailed_text",
                "secondary": "written_exercises",
                "avoid": "audio_only_content"
            }
        }
        
        return format_preferences.get(self.learning_style, format_preferences["Visual"])
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get learning progress summary"""
        if not self.learning_history:
            return {
                "total_sessions": 0,
                "total_time": 0,
                "average_satisfaction": 0,
                "topics_covered": [],
                "progress_trend": "no_data"
            }
        
        total_sessions = len(self.learning_history)
        total_time = sum(session.get("duration", 0) for session in self.learning_history)
        
        satisfactions = [s.get("satisfaction_score") for s in self.learning_history 
                        if s.get("satisfaction_score") is not None]
        avg_satisfaction = sum(satisfactions) / len(satisfactions) if satisfactions else 0
        
        all_topics = []
        for session in self.learning_history:
            all_topics.extend(session.get("topics_covered", []))
        unique_topics = list(set(all_topics))
        
        # Simple progress trend analysis
        recent_sessions = self.learning_history[-5:] if len(self.learning_history) >= 5 else self.learning_history
        recent_satisfaction = [s.get("satisfaction_score") for s in recent_sessions 
                             if s.get("satisfaction_score") is not None]
        
        if len(recent_satisfaction) >= 2:
            if recent_satisfaction[-1] > recent_satisfaction[0]:
                trend = "improving"
            elif recent_satisfaction[-1] < recent_satisfaction[0]:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "total_sessions": total_sessions,
            "total_time": total_time,
            "average_satisfaction": round(avg_satisfaction, 2),
            "topics_covered": unique_topics,
            "progress_trend": trend
        }
    
    def save_profile(self):
        """Save profile to file"""
        try:
            profile_data = {
                "name": self.name,
                "learning_style": self.learning_style,
                "subjects": self.subjects,
                "preferences": self.preferences,
                "learning_history": self.learning_history,
                "created_at": self.created_at,
                "last_updated": self.last_updated
            }
            
            with open(self.profile_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving profile: {e}")
    
    def load_profile(self):
        """Load profile from file"""
        try:
            if os.path.exists(self.profile_file):
                with open(self.profile_file, 'r') as f:
                    profile_data = json.load(f)
                
                self.name = profile_data.get("name", "")
                self.learning_style = profile_data.get("learning_style", "Visual")
                self.subjects = profile_data.get("subjects", [])
                self.preferences = profile_data.get("preferences", {})
                self.learning_history = profile_data.get("learning_history", [])
                self.created_at = profile_data.get("created_at", datetime.now().isoformat())
                self.last_updated = profile_data.get("last_updated", datetime.now().isoformat())
                
        except Exception as e:
            print(f"Error loading profile: {e}")
    
    def reset_profile(self):
        """Reset profile to defaults"""
        self.name = ""
        self.learning_style = "Visual"
        self.subjects = []
        self.preferences = {}
        self.learning_history = []
        self.created_at = datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()
        
        # Remove profile file
        if os.path.exists(self.profile_file):
            os.remove(self.profile_file)
    
    def export_profile(self) -> Dict[str, Any]:
        """Export profile data"""
        return {
            "name": self.name,
            "learning_style": self.learning_style,
            "subjects": self.subjects,
            "preferences": self.preferences,
            "learning_history": self.learning_history,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "progress_summary": self.get_progress_summary()
        }