"""
AI Educational Assistant - Dashboard Module
Comprehensive dashboard with progress charts, recommended modules, and personalized greeting
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Any
import random

@dataclass
class DashboardMetrics:
    """Data class for dashboard metrics"""
    daily_questions: int
    study_streak: int
    topics_mastered: int
    learning_score: int
    total_sessions: int
    average_session_time: float
    weekly_progress: List[int]
    subject_progress: Dict[str, int]

@dataclass
class RecommendedModule:
    """Data class for recommended learning modules"""
    title: str
    subject: str
    difficulty: str
    estimated_time: int
    progress: int
    description: str
    icon: str

@dataclass
class RecentActivity:
    """Data class for recent learning activities"""
    activity_type: str
    title: str
    timestamp: datetime
    score: int
    icon: str

class DashboardManager:
    """Manages dashboard data and analytics"""
    
    def __init__(self, analytics):
        self.analytics = analytics
    
    def get_dashboard_metrics(self) -> DashboardMetrics:
        """Get comprehensive dashboard metrics"""
        # Get basic analytics
        analytics_data = self.analytics.get_summary()
        
        # Generate sample data for demonstration
        return DashboardMetrics(
            daily_questions=analytics_data.get('daily_questions', random.randint(5, 25)),
            study_streak=analytics_data.get('streak_days', random.randint(1, 15)),
            topics_mastered=analytics_data.get('mastered_topics', random.randint(2, 8)),
            learning_score=analytics_data.get('learning_score', random.randint(65, 95)),
            total_sessions=analytics_data.get('total_sessions', random.randint(10, 50)),
            average_session_time=analytics_data.get('avg_session_time', random.uniform(15.0, 45.0)),
            weekly_progress=[random.randint(60, 100) for _ in range(7)],
            subject_progress={
                'Python': random.randint(70, 95),
                'Mathematics': random.randint(60, 85),
                'Data Science': random.randint(40, 75),
                'Machine Learning': random.randint(30, 60)
            }
        )
    
    def get_recommended_modules(self, user_profile: Dict) -> List[RecommendedModule]:
        """Get personalized module recommendations"""
        subjects = user_profile.get('subjects', ['Python', 'Mathematics'])
        learning_style = user_profile.get('learning_style', 'visual')
        
        # Sample recommendations based on user profile
        all_modules = [
            RecommendedModule(
                title="Python Functions Deep Dive",
                subject="Python",
                difficulty="Intermediate",
                estimated_time=30,
                progress=0,
                description="Master function definitions, parameters, and advanced concepts",
                icon="🐍"
            ),
            RecommendedModule(
                title="Data Structures Fundamentals",
                subject="Computer Science",
                difficulty="Beginner",
                estimated_time=45,
                progress=25,
                description="Learn about lists, dictionaries, sets, and tuples",
                icon="📊"
            ),
            RecommendedModule(
                title="Linear Algebra Basics",
                subject="Mathematics",
                difficulty="Intermediate",
                estimated_time=60,
                progress=0,
                description="Vectors, matrices, and linear transformations",
                icon="📐"
            ),
            RecommendedModule(
                title="Machine Learning Introduction",
                subject="Data Science",
                difficulty="Advanced",
                estimated_time=90,
                progress=0,
                description="Supervised and unsupervised learning concepts",
                icon="🤖"
            )
        ]
        
        # Filter based on user subjects
        recommended = [module for module in all_modules 
                      if any(subject.lower() in module.subject.lower() for subject in subjects)]
        
        return recommended[:3]  # Return top 3 recommendations
    
    def get_recent_activities(self) -> List[RecentActivity]:
        """Get recent learning activities"""
        # Sample recent activities
        activities = [
            RecentActivity(
                activity_type="Quiz",
                title="Python Basics Quiz",
                timestamp=datetime.now() - timedelta(hours=2),
                score=85,
                icon="📝"
            ),
            RecentActivity(
                activity_type="Chat",
                title="Asked about loops",
                timestamp=datetime.now() - timedelta(hours=5),
                score=0,
                icon="💬"
            ),
            RecentActivity(
                activity_type="Module",
                title="Completed Variables lesson",
                timestamp=datetime.now() - timedelta(days=1),
                score=92,
                icon="📚"
            ),
            RecentActivity(
                activity_type="Practice",
                title="Coding exercises",
                timestamp=datetime.now() - timedelta(days=2),
                score=78,
                icon="💻"
            )
        ]
        
        return activities

class DashboardInterface:
    """Streamlit interface for the dashboard"""
    
    def __init__(self, dashboard_manager: DashboardManager):
        self.dashboard_manager = dashboard_manager
    
    def render_dashboard(self):
        """Render the complete dashboard interface"""
        # Get user profile
        user_profile = st.session_state.get('user_profile', {})
        
        # Personalized greeting
        self._render_greeting(user_profile)
        
        # Dashboard metrics
        metrics = self.dashboard_manager.get_dashboard_metrics()
        self._render_metrics_cards(metrics)
        
        st.divider()
        
        # Main dashboard content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Progress charts
            self._render_progress_charts(metrics)
            
            # Recommended modules
            self._render_recommended_modules(user_profile)
        
        with col2:
            # Quick actions
            self._render_quick_actions()
            
            # Recent activity
            self._render_recent_activity()
    
    def _render_greeting(self, user_profile: Dict):
        """Render personalized greeting"""
        user_name = user_profile.get('name', 'Learner')
        current_hour = datetime.now().hour
        
        if current_hour < 12:
            greeting = "Good morning"
            emoji = "🌅"
        elif current_hour < 17:
            greeting = "Good afternoon"
            emoji = "☀️"
        else:
            greeting = "Good evening"
            emoji = "🌙"
        
        st.markdown(f"## {greeting}, {user_name}! {emoji}")
        st.markdown("Ready to continue your learning journey?")
    
    def _render_metrics_cards(self, metrics: DashboardMetrics):
        """Render dashboard metrics cards"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Questions Today",
                metrics.daily_questions,
                delta=random.randint(-2, 5)
            )
        
        with col2:
            st.metric(
                "Study Streak",
                f"{metrics.study_streak} days",
                delta=1 if metrics.study_streak > 0 else 0
            )
        
        with col3:
            st.metric(
                "Topics Mastered",
                metrics.topics_mastered,
                delta=random.randint(0, 2)
            )
        
        with col4:
            st.metric(
                "Learning Score",
                f"{metrics.learning_score}/100",
                delta=random.randint(-3, 7)
            )
    
    def _render_progress_charts(self, metrics: DashboardMetrics):
        """Render progress visualization charts"""
        st.subheader("📈 Progress Overview")
        
        # Weekly progress chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Weekly Learning Progress**")
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            fig_weekly = px.line(
                x=days,
                y=metrics.weekly_progress,
                title="Daily Progress (%)",
                markers=True
            )
            fig_weekly.update_layout(
                height=300,
                showlegend=False,
                title_font_size=14
            )
            st.plotly_chart(fig_weekly, use_container_width=True)
        
        with col2:
            st.markdown("**Subject Progress**")
            
            fig_subjects = px.bar(
                x=list(metrics.subject_progress.keys()),
                y=list(metrics.subject_progress.values()),
                title="Progress by Subject (%)",
                color=list(metrics.subject_progress.values()),
                color_continuous_scale="viridis"
            )
            fig_subjects.update_layout(
                height=300,
                showlegend=False,
                title_font_size=14
            )
            st.plotly_chart(fig_subjects, use_container_width=True)
    
    def _render_recommended_modules(self, user_profile: Dict):
        """Render recommended learning modules"""
        st.subheader("📚 Recommended for You")
        
        modules = self.dashboard_manager.get_recommended_modules(user_profile)
        
        for module in modules:
            with st.container():
                col1, col2, col3 = st.columns([1, 4, 2])
                
                with col1:
                    st.markdown(f"## {module.icon}")
                
                with col2:
                    st.markdown(f"**{module.title}**")
                    st.markdown(f"*{module.subject} • {module.difficulty} • {module.estimated_time} min*")
                    st.markdown(module.description)
                    
                    if module.progress > 0:
                        st.progress(module.progress / 100)
                        st.caption(f"Progress: {module.progress}%")
                
                with col3:
                    if st.button(
                        "Start" if module.progress == 0 else "Continue",
                        key=f"module_{module.title}",
                        use_container_width=True
                    ):
                        st.success(f"Starting {module.title}...")
                
                st.divider()
    
    def _render_quick_actions(self):
        """Render quick action buttons"""
        st.subheader("⚡ Quick Actions")
        
        actions = [
            {"label": "📚 Start Learning", "page": "learn", "color": "primary"},
            {"label": "💬 Ask AI Tutor", "page": "chat", "color": "secondary"},
            {"label": "📝 Take Quiz", "page": "learn", "color": "secondary"},
            {"label": "👤 Edit Profile", "page": "profile", "color": "secondary"}
        ]
        
        for action in actions:
            if st.button(
                action["label"],
                key=f"action_{action['label']}",
                use_container_width=True,
                type=action["color"]
            ):
                st.session_state.current_page = action["page"]
                st.rerun()
    
    def _render_recent_activity(self):
        """Render recent learning activities"""
        st.subheader("🕒 Recent Activity")
        
        activities = self.dashboard_manager.get_recent_activities()
        
        for activity in activities:
            with st.container():
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    st.markdown(f"## {activity.icon}")
                
                with col2:
                    st.markdown(f"**{activity.title}**")
                    st.caption(f"{activity.activity_type} • {activity.timestamp.strftime('%H:%M')}")
                    
                    if activity.score > 0:
                        st.caption(f"Score: {activity.score}%")
                
                st.divider()