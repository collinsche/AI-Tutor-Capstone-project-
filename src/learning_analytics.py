#!/usr/bin/env python3
"""
Learning Analytics Module
Tracks user progress, engagement, and learning patterns
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import statistics

class LearningAnalytics:
    """Learning analytics and progress tracking class"""
    
    def __init__(self, analytics_file: str = "learning_analytics.json"):
        """Initialize learning analytics"""
        self.analytics_file = analytics_file
        self.interactions = []
        self.sessions = []
        self.current_session = None
        self.load_analytics()
    
    def start_session(self, user_id: str = "default_user"):
        """Start a new learning session"""
        self.current_session = {
            "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": user_id,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration_minutes": 0,
            "interactions_count": 0,
            "topics_covered": set(),
            "questions_asked": [],
            "responses_generated": [],
            "engagement_score": 0
        }
    
    def end_session(self):
        """End the current learning session"""
        if self.current_session:
            self.current_session["end_time"] = datetime.now().isoformat()
            
            # Calculate duration
            start_time = datetime.fromisoformat(self.current_session["start_time"])
            end_time = datetime.fromisoformat(self.current_session["end_time"])
            duration = (end_time - start_time).total_seconds() / 60
            self.current_session["duration_minutes"] = round(duration, 2)
            
            # Convert set to list for JSON serialization
            self.current_session["topics_covered"] = list(self.current_session["topics_covered"])
            
            # Calculate engagement score
            self.current_session["engagement_score"] = self._calculate_engagement_score()
            
            # Add to sessions list
            self.sessions.append(self.current_session.copy())
            self.current_session = None
            
            # Save analytics
            self.save_analytics()
    
    def log_interaction(self, user_input: str, ai_response: str, 
                       topics: Optional[List[str]] = None):
        """Log a user-AI interaction"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response,
            "input_length": len(user_input),
            "response_length": len(ai_response),
            "topics": topics or self._extract_topics(user_input),
            "interaction_type": self._classify_interaction(user_input),
            "complexity_score": self._calculate_complexity(user_input)
        }
        
        self.interactions.append(interaction)
        
        # Update current session if active
        if self.current_session:
            self.current_session["interactions_count"] += 1
            self.current_session["questions_asked"].append(user_input)
            self.current_session["responses_generated"].append(ai_response)
            if topics:
                self.current_session["topics_covered"].update(topics)
        
        # Auto-save every 10 interactions
        if len(self.interactions) % 10 == 0:
            self.save_analytics()
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from user input using keyword matching"""
        topic_keywords = {
            "mathematics": ["math", "algebra", "calculus", "geometry", "statistics", "equation", "formula"],
            "science": ["physics", "chemistry", "biology", "experiment", "hypothesis", "theory"],
            "history": ["history", "historical", "war", "civilization", "empire", "revolution"],
            "literature": ["literature", "poetry", "novel", "author", "writing", "story"],
            "computer_science": ["programming", "code", "algorithm", "software", "computer", "data"],
            "languages": ["language", "grammar", "vocabulary", "translation", "pronunciation"]
        }
        
        detected_topics = []
        text_lower = text.lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics if detected_topics else ["general"]
    
    def _classify_interaction(self, user_input: str) -> str:
        """Classify the type of user interaction"""
        text_lower = user_input.lower()
        
        if any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where', '?']):
            return "question"
        elif any(word in text_lower for word in ['help', 'explain', 'teach', 'show']):
            return "help_request"
        elif any(word in text_lower for word in ['practice', 'exercise', 'problem', 'solve']):
            return "practice_request"
        elif any(word in text_lower for word in ['thank', 'thanks', 'good', 'great']):
            return "feedback"
        else:
            return "general"
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate complexity score of user input (0-1)"""
        # Simple complexity based on length and vocabulary
        word_count = len(text.split())
        char_count = len(text)
        
        # Normalize scores
        word_score = min(word_count / 50, 1.0)  # Max at 50 words
        char_score = min(char_count / 500, 1.0)  # Max at 500 chars
        
        # Check for complex terms
        complex_indicators = ['analyze', 'evaluate', 'synthesize', 'compare', 'contrast', 
                            'explain', 'demonstrate', 'calculate', 'derive', 'prove']
        complexity_bonus = sum(1 for word in complex_indicators if word in text.lower()) * 0.1
        
        return min((word_score + char_score) / 2 + complexity_bonus, 1.0)
    
    def _calculate_engagement_score(self) -> float:
        """Calculate engagement score for current session (0-1)"""
        if not self.current_session:
            return 0.0
        
        # Factors for engagement
        interaction_score = min(self.current_session["interactions_count"] / 20, 1.0)
        duration_score = min(self.current_session["duration_minutes"] / 60, 1.0)
        topic_diversity = min(len(self.current_session["topics_covered"]) / 5, 1.0)
        
        # Average complexity of questions
        if self.current_session["questions_asked"]:
            avg_complexity = statistics.mean(
                self._calculate_complexity(q) for q in self.current_session["questions_asked"]
            )
        else:
            avg_complexity = 0
        
        # Weighted engagement score
        engagement = (
            interaction_score * 0.3 +
            duration_score * 0.2 +
            topic_diversity * 0.2 +
            avg_complexity * 0.3
        )
        
        return round(engagement, 3)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get analytics summary"""
        total_interactions = len(self.interactions)
        total_sessions = len(self.sessions)
        
        if total_sessions == 0:
            return {
                "total_questions": total_interactions,
                "sessions": 0,
                "avg_time": 0,
                "progress": 0,
                "engagement_trend": "no_data"
            }
        
        # Calculate averages
        avg_session_time = statistics.mean(s["duration_minutes"] for s in self.sessions)
        avg_engagement = statistics.mean(s["engagement_score"] for s in self.sessions)
        
        # Progress calculation (simple linear growth based on sessions and engagement)
        progress = min((total_sessions * 0.1) + (avg_engagement * 0.5), 1.0)
        
        return {
            "total_questions": total_interactions,
            "sessions": total_sessions,
            "avg_time": round(avg_session_time, 1),
            "progress": round(progress, 2),
            "engagement_trend": self._get_engagement_trend()
        }
    
    def _get_engagement_trend(self) -> str:
        """Analyze engagement trend over recent sessions"""
        if len(self.sessions) < 3:
            return "insufficient_data"
        
        recent_sessions = self.sessions[-5:]  # Last 5 sessions
        engagement_scores = [s["engagement_score"] for s in recent_sessions]
        
        # Simple trend analysis
        if len(engagement_scores) >= 3:
            recent_avg = statistics.mean(engagement_scores[-3:])
            earlier_avg = statistics.mean(engagement_scores[:-3]) if len(engagement_scores) > 3 else engagement_scores[0]
            
            if recent_avg > earlier_avg + 0.1:
                return "improving"
            elif recent_avg < earlier_avg - 0.1:
                return "declining"
            else:
                return "stable"
        
        return "stable"
    
    def get_detailed_analytics(self) -> Dict[str, Any]:
        """Get detailed analytics report"""
        if not self.interactions:
            return {"message": "No interaction data available"}
        
        # Topic analysis
        all_topics = []
        for interaction in self.interactions:
            all_topics.extend(interaction.get("topics", []))
        
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Interaction type analysis
        interaction_types = {}
        for interaction in self.interactions:
            itype = interaction.get("interaction_type", "general")
            interaction_types[itype] = interaction_types.get(itype, 0) + 1
        
        # Time-based analysis
        daily_activity = self._analyze_daily_activity()
        
        # Learning patterns
        learning_patterns = self._analyze_learning_patterns()
        
        return {
            "total_interactions": len(self.interactions),
            "total_sessions": len(self.sessions),
            "topic_distribution": topic_counts,
            "interaction_types": interaction_types,
            "daily_activity": daily_activity,
            "learning_patterns": learning_patterns,
            "average_complexity": self._get_average_complexity(),
            "engagement_metrics": self._get_engagement_metrics()
        }
    
    def _analyze_daily_activity(self) -> Dict[str, int]:
        """Analyze daily activity patterns"""
        daily_counts = {}
        
        for interaction in self.interactions:
            timestamp = interaction.get("timestamp", "")
            if timestamp:
                try:
                    date = datetime.fromisoformat(timestamp).date().isoformat()
                    daily_counts[date] = daily_counts.get(date, 0) + 1
                except:
                    continue
        
        return daily_counts
    
    def _analyze_learning_patterns(self) -> Dict[str, Any]:
        """Analyze learning patterns and preferences"""
        if not self.sessions:
            return {}
        
        # Session duration patterns
        durations = [s["duration_minutes"] for s in self.sessions]
        
        # Peak activity hours
        hour_counts = {}
        for session in self.sessions:
            start_time = session.get("start_time", "")
            if start_time:
                try:
                    hour = datetime.fromisoformat(start_time).hour
                    hour_counts[hour] = hour_counts.get(hour, 0) + 1
                except:
                    continue
        
        peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "average_session_duration": round(statistics.mean(durations), 2) if durations else 0,
            "session_duration_range": [min(durations), max(durations)] if durations else [0, 0],
            "peak_learning_hours": [hour for hour, count in peak_hours],
            "total_learning_time": round(sum(durations), 2)
        }
    
    def _get_average_complexity(self) -> float:
        """Get average complexity score of all interactions"""
        if not self.interactions:
            return 0.0
        
        complexities = [i.get("complexity_score", 0) for i in self.interactions]
        return round(statistics.mean(complexities), 3)
    
    def _get_engagement_metrics(self) -> Dict[str, float]:
        """Get engagement metrics"""
        if not self.sessions:
            return {}
        
        engagement_scores = [s["engagement_score"] for s in self.sessions]
        
        return {
            "average_engagement": round(statistics.mean(engagement_scores), 3),
            "max_engagement": round(max(engagement_scores), 3),
            "min_engagement": round(min(engagement_scores), 3),
            "engagement_std_dev": round(statistics.stdev(engagement_scores), 3) if len(engagement_scores) > 1 else 0
        }
    
    def save_analytics(self):
        """Save analytics data to file"""
        try:
            analytics_data = {
                "interactions": self.interactions,
                "sessions": self.sessions,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.analytics_file, 'w') as f:
                json.dump(analytics_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving analytics: {e}")
    
    def load_analytics(self):
        """Load analytics data from file"""
        try:
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    analytics_data = json.load(f)
                
                self.interactions = analytics_data.get("interactions", [])
                self.sessions = analytics_data.get("sessions", [])
                
        except Exception as e:
            print(f"Error loading analytics: {e}")
    
    def reset_analytics(self):
        """Reset all analytics data"""
        self.interactions = []
        self.sessions = []
        self.current_session = None
        
        if os.path.exists(self.analytics_file):
            os.remove(self.analytics_file)
    
    def export_analytics(self) -> Dict[str, Any]:
        """Export all analytics data"""
        return {
            "interactions": self.interactions,
            "sessions": self.sessions,
            "summary": self.get_summary(),
            "detailed_analytics": self.get_detailed_analytics(),
            "export_timestamp": datetime.now().isoformat()
        }