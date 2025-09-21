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
        self.subjects: List[str] = []
        self.preferences: Dict[str, Any] = {}
        self.learning_history: List[Dict[str, Any]] = []
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
        """Get personalized learning preferences"""
        return {
            "learning_style": self.learning_style,
            "preferred_subjects": self.subjects,
            "difficulty_preference": self.preferences.get("difficulty", "adaptive"),
            "session_length": self._analyze_session_length(),
            "best_time": self._analyze_best_learning_time(),
            "content_format": self.preferences.get("content_format", "mixed")
        }

    def _analyze_best_learning_time(self) -> str:
        """Analyze best learning time based on session history"""
        if not self.learning_history:
            return "morning"  # Default recommendation
        
        # Simple analysis based on satisfaction scores by time of day
        time_satisfaction: Dict[str, List[float]] = {"morning": [], "afternoon": [], "evening": []}
        
        for session in self.learning_history:
            try:
                session_time = datetime.fromisoformat(session["timestamp"])
                hour = session_time.hour
                satisfaction = session.get("satisfaction_score")
                
                if satisfaction is not None:
                    if 6 <= hour < 12:
                        time_satisfaction["morning"].append(satisfaction)
                    elif 12 <= hour < 18:
                        time_satisfaction["afternoon"].append(satisfaction)
                    else:
                        time_satisfaction["evening"].append(satisfaction)
            except (ValueError, KeyError):
                continue
        
        # Find time with highest average satisfaction
        best_time = "morning"
        best_score = 0
        
        for time_period, scores in time_satisfaction.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score > best_score:
                    best_score = avg_score
                    best_time = time_period
        
        return best_time

    def _analyze_session_length(self) -> int:
        """Analyze preferred session length in minutes"""
        if not self.learning_history:
            return 30  # Default 30 minutes
        
        durations = [session.get("duration", 30) for session in self.learning_history]
        avg_duration = sum(durations) / len(durations)
        
        return int(avg_duration)

    def get_subject_interests(self) -> List[str]:
        """Get list of subject interests"""
        return self.subjects.copy()

    def add_subject_interest(self, subject: str):
        """Add a new subject interest"""
        if subject not in self.subjects:
            self.subjects.append(subject)
            self.last_updated = datetime.now().isoformat()
            self.save_profile()

    def remove_subject_interest(self, subject: str):
        """Remove a subject interest"""
        if subject in self.subjects:
            self.subjects.remove(subject)
            self.last_updated = datetime.now().isoformat()
            self.save_profile()

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        if not self.learning_history:
            return {
                "total_sessions": 0,
                "total_time": 0,
                "average_session": 0,
                "favorite_subjects": [],
                "learning_streak": 0
            }
        
        total_sessions = len(self.learning_history)
        total_time = sum(session.get("duration", 0) for session in self.learning_history)
        avg_session = total_time / total_sessions if total_sessions > 0 else 0
        
        # Analyze favorite subjects
        subject_counts: Dict[str, int] = {}
        for session in self.learning_history:
            topics = session.get("topics_covered", [])
            for topic in topics:
                subject_counts[topic] = subject_counts.get(topic, 0) + 1
        
        favorite_subjects = sorted(subject_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "total_sessions": total_sessions,
            "total_time": total_time,
            "average_session": round(avg_session, 1),
            "favorite_subjects": [subject for subject, _ in favorite_subjects],
            "learning_streak": self._calculate_streak()
        }

    def _calculate_streak(self) -> int:
        """Calculate current learning streak"""
        if not self.learning_history:
            return 0
        
        # Sort sessions by date
        sorted_sessions = sorted(self.learning_history, key=lambda x: x.get("timestamp", ""), reverse=True)
        
        streak = 0
        current_date = datetime.now().date()
        
        for session in sorted_sessions:
            try:
                session_date = datetime.fromisoformat(session["timestamp"]).date()
                
                if session_date == current_date or (current_date - session_date).days == streak + 1:
                    streak += 1
                    current_date = session_date
                else:
                    break
            except (ValueError, KeyError):
                continue
        
        return streak

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

    def get(self, key: str, default=None):
        """Get attribute value with default fallback (dict-like interface)"""
        return getattr(self, key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary format"""
        return {
            "name": self.name,
            "learning_style": self.learning_style,
            "subjects": self.subjects,
            "preferences": self.preferences,
            "learning_history": self.learning_history,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "user_id": getattr(self, 'user_id', self.name),  # Add user_id support
            "knowledge_level": getattr(self, 'knowledge_level', {}),  # Add knowledge_level support
            "available_time": getattr(self, 'available_time', 60),  # Add available_time support
            "goals": getattr(self, 'goals', []),  # Add goals support
            "experience_level": getattr(self, 'experience_level', 'Beginner'),  # Add experience_level support
            "email": getattr(self, 'email', '')  # Add email support
        }
    
    def export_profile(self) -> Dict[str, Any]:
        """Export profile data"""
        profile_dict = self.to_dict()
        profile_dict["progress_summary"] = self.get_progress_summary()
        return profile_dict