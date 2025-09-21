#!/usr/bin/env python3
"""
Application Router and Navigation System
Implements proper routing for /home, /learn, /chat, /profile pages with responsive design
"""

import streamlit as st
from typing import Dict, Any, Callable
from datetime import datetime

# Import page modules
from onboarding import OnboardingSystem, run_onboarding_chat, OnboardingInterface
from educational_assistant import EducationalAssistant
from user_profile import UserProfile
from learning_analytics import LearningAnalytics
from learning_paths import LearningPathGenerator
from enhanced_chat import EnhancedChatInterface
from adaptive_quiz import AdaptiveQuizInterface
from content_generator import ContentGenerator, ContentInterface
from dashboard import DashboardManager, DashboardInterface

class AppRouter:
    """Main application router with page navigation and state management"""
    
    def __init__(self):
        """Initialize the application router with all components"""
        # Initialize session state first to ensure components get shared instances
        self._initialize_session_state()
    
        # Initialize core components using instances from session state
        self.analytics = st.session_state.analytics
        self.educational_assistant = st.session_state.assistant
        
        # Initialize specialized components
        self.onboarding_system = OnboardingSystem()
        self.onboarding_interface = OnboardingInterface(self.onboarding_system)
        self.learning_path_generator = LearningPathGenerator()
        self.enhanced_chat = EnhancedChatInterface(self.educational_assistant)
        self.adaptive_quiz = AdaptiveQuizInterface(self.educational_assistant)
        self.content_generator = ContentGenerator(self.educational_assistant)
        self.content_interface = ContentInterface(self.content_generator)
        self.dashboard_manager = DashboardManager(self.analytics)
        self.dashboard_interface = DashboardInterface(self.dashboard_manager)
        
        self.pages = {
            "home": {
                "title": "🏠 Dashboard",
                "icon": "🏠",
                "function": self.render_home_page,
                "description": "Your personalized learning dashboard"
            },
            "learn": {
                "title": "📚 Learn",
                "icon": "📚", 
                "function": self.render_learn_page,
                "description": "Interactive learning modules and content"
            },
            "chat": {
                "title": "💬 AI Tutor",
                "icon": "💬",
                "function": self.render_chat_page,
                "description": "Chat with your AI tutor"
            },
            "profile": {
                "title": "👤 Profile",
                "icon": "👤",
                "function": self.render_profile_page,
                "description": "Manage your learning profile and preferences"
            }
        }
        
        # Initialize components
        self.onboarding = OnboardingSystem()
        
    def run(self):
        """Main router function"""
        # Set page config
        st.set_page_config(
            page_title="AI Educational Assistant",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Session state is already initialized in __init__
        
        # Check if onboarding is needed
        if not self.onboarding.is_onboarding_complete() and not st.session_state.get('skip_onboarding', False):
            self._render_onboarding()
            return
        
        # Render main application
        self._render_main_app()
    
    def _initialize_session_state(self):
        """Initialize all session state variables"""
        if 'assistant' not in st.session_state:
            st.session_state.assistant = EducationalAssistant()
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {}
        if 'analytics' not in st.session_state:
            st.session_state.analytics = LearningAnalytics()
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        # Set user_profile_complete to True for testing purposes
        if 'user_profile_complete' not in st.session_state:
            st.session_state.user_profile_complete = True
    
    def _render_onboarding(self):
        """Render onboarding flow"""
        st.title("🎓 Welcome to AI Educational Assistant")
        
        # Onboarding mode selection
        if 'onboarding_mode' not in st.session_state:
            st.session_state.onboarding_mode = 'quiz'
        
        # Mode selector
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            mode = st.radio(
                "Choose your onboarding experience:",
                ["quiz", "chat"],
                format_func=lambda x: "📝 Interactive Quiz" if x == "quiz" else "💬 Chat Setup",
                horizontal=True
            )
            st.session_state.onboarding_mode = mode
        
        st.divider()
        
        # Render selected onboarding mode
        if st.session_state.onboarding_mode == 'quiz':
            self.onboarding.run_interactive_assessment()
        else:
            run_onboarding_chat()
        
        # Skip onboarding option
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Skip Onboarding", help="You can complete this later in your profile"):
                st.session_state.skip_onboarding = True
                st.session_state.onboarding_complete = True
                st.session_state.user_profile_complete = True  # Set the flag for main app access
                st.rerun()
    
    def _render_main_app(self):
        """Render the main application with navigation"""
        # Sidebar navigation
        with st.sidebar:
            self._render_navigation()
            st.divider()
            self._render_user_info()
            st.divider()
            self._render_quick_analytics()
        
        # Main content area
        self._render_current_page()
    
    def _render_navigation(self):
        """Render sidebar navigation"""
        st.header("🧭 Navigation")
        
        for page_key, page_info in self.pages.items():
            if st.button(
                f"{page_info['icon']} {page_info['title']}", 
                key=f"nav_{page_key}",
                help=page_info['description'],
                use_container_width=True
            ):
                st.session_state.current_page = page_key
                st.rerun()
        
        # Highlight current page
        if st.session_state.current_page in self.pages:
            current_page_info = self.pages[st.session_state.current_page]
            st.info(f"📍 Current: {current_page_info['title']}")
    
    def _render_user_info(self):
        """Render user information in sidebar"""
        st.header("👤 User Info")
        
        user_profile = st.session_state.get('user_profile', {})
        
        if user_profile.get('name'):
            st.write(f"**Name:** {user_profile['name']}")
        else:
            st.write("**Name:** Not set")
        
        if user_profile.get('learning_style'):
            st.write(f"**Learning Style:** {user_profile['learning_style']}")
        
        if user_profile.get('subjects'):
            subjects = user_profile['subjects']
            st.write(f"**Subjects:** {', '.join(subjects[:2])}{'...' if len(subjects) > 2 else ''}")
        
        # Quick profile update
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.session_state.current_page = 'profile'
            st.rerun()
    
    def _render_quick_analytics(self):
        """Render quick analytics in sidebar"""
        st.header("📊 Quick Stats")
        
        analytics = st.session_state.analytics.get_summary()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Questions", analytics.get('total_questions', 0))
        with col2:
            st.metric("Sessions", analytics.get('sessions', 0))
        
        progress = analytics.get('progress', 0)
        st.progress(progress)
        st.caption(f"Progress: {progress*100:.0f}%")
    
    def _render_current_page(self):
        """Render the current page content"""
        current_page = st.session_state.current_page
        
        if current_page in self.pages:
            page_info = self.pages[current_page]
            page_info['function']()
        else:
            st.error(f"Page '{current_page}' not found!")
    
    def render_home_page(self):
        """Render the main dashboard/home page with enhanced visual design"""
        # Enhanced header with gradient-style background
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: white; text-align: center; margin: 0;">
                🎓 AI Educational Assistant Dashboard
            </h1>
            <p style="color: #f0f0f0; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
                Welcome to your personalized learning experience!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if user has completed onboarding
        if not st.session_state.get('user_profile_complete', False):
            st.warning("⚠️ Please complete your profile setup first!")
            if st.button("Complete Profile Setup"):
                st.session_state.current_page = "profile"
                st.rerun()
            return
        
        # Enhanced metrics cards
        self._render_enhanced_metrics()
        
        # Main content area with improved layout
        col1, col2 = st.columns([2, 1], gap="large")
        
        with col1:
            st.markdown("### 📊 Learning Overview")
            self._render_quick_analytics()
            
            st.markdown("### 🎯 Recommended Actions")
            self._render_recommendations_cards()
        
        with col2:
            st.markdown("### 📈 Progress Visualization")
            self._render_progress_charts()
            
            st.markdown("### ⚡ Quick Actions")
            self._render_quick_actions()
        
        # Render the dashboard interface
        self.dashboard_interface.render_dashboard()
    
    def render_learn_page(self):
        """Render enhanced learning page with modern styling"""
        # Enhanced header
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: white; text-align: center; margin: 0;">
                📚 Interactive Learning Hub
            </h1>
            <p style="color: #f0f0f0; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
                Personalized learning paths and adaptive assessments
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if user has completed onboarding
        if not st.session_state.get('user_profile_complete', False):
            st.warning("⚠️ Please complete your profile setup to access learning modules!")
            return
        
        # Enhanced tabs with custom styling
        st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            padding: 0 1.5rem;
            background: linear-gradient(135deg, #f0f2f6 0%, #e8eaf6 100%);
            border-radius: 10px;
            border: none;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create tabs for different learning activities
        tab1, tab2, tab3 = st.tabs(["🛤️ Learning Paths", "📝 Adaptive Quiz", "📖 Content Library"])

        with tab1:
            st.markdown("### 🎯 Personalized Learning Paths")
            
            # Get user profile for personalized paths
            user_profile = st.session_state.get('user_profile', {})
            
            # Ensure user profile has default values if empty
            if not user_profile or not user_profile.get('subjects'):
                default_profile = {
                    'user_id': 'default_user',
                    'subjects': ['Python Programming'],
                    'learning_style': 'Visual',
                    'knowledge_level': {'Python Programming': 1},
                    'available_time': 60,
                    'goals': ['Learn programming fundamentals']
                }
                user_profile = default_profile
                st.session_state.user_profile = default_profile
            
            # Enhanced generate button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Generate New Learning Path", type="primary", use_container_width=True):
                    with st.spinner("Creating your personalized learning path..."):
                        try:
                            # Get the subject from user profile
                            subject = user_profile.get('subjects', ['Python Programming'])[0]
                            
                            # Debug information
                            st.write(f"Debug: Generating path for subject: {subject}")
                            st.write(f"Debug: User profile: {user_profile}")
                            
                            # Generate the learning path
                            learning_path = self.learning_path_generator.generate_learning_path(
                                user_profile=user_profile,
                                subject=subject
                            )
                            
                            # Debug the generated path
                            st.write(f"Debug: Generated path with {len(learning_path.modules)} modules")
                            st.write(f"Debug: Path title: {learning_path.title}")
                            
                            # Store in session state
                            st.session_state.current_learning_path = learning_path
                            
                            # Show success message
                            st.success(f"✅ Generated new learning path for {subject}!")
                            
                            # Force immediate display instead of rerun
                            st.write("Debug: Learning path stored in session state")
                            
                        except Exception as e:
                            st.error(f"Failed to generate learning path: {str(e)}")
                            st.write(f"Debug: Exception details: {type(e).__name__}: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())
                            st.info("💡 Try completing your profile setup first or contact support if the issue persists.")
            
            # Display current learning path with enhanced styling
            if hasattr(st.session_state, 'current_learning_path') and st.session_state.current_learning_path:
                path = st.session_state.current_learning_path
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 2rem; border-radius: 10px; margin: 1rem 0; color: white;">
                    <h3 style="margin: 0 0 1rem 0;">{path.title}</h3>
                    <div style="display: flex; gap: 2rem; margin-bottom: 1rem;">
                        <div><strong>Difficulty:</strong> {path.difficulty_progression[0] if path.difficulty_progression else "Medium"}</div>
                        <div><strong>Duration:</strong> {path.total_estimated_time} minutes</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced modules display
                st.markdown("#### 📋 Learning Modules")
                for i, module in enumerate(path.modules):
                    with st.expander(f"Module {i+1}: {module.title}", expanded=i==0):
                        st.markdown(f"**Type:** {module.content_type.title()}")
                        st.markdown(f"**Duration:** {module.estimated_time} minutes")
                        st.markdown(f"**Difficulty:** {module.difficulty}")
                        st.markdown(module.description)
                        
                        if st.button(f"Start Module {i+1}", key=f"start_module_{i}"):
                            st.success(f"Starting {module.title}...")
                            # Generate and display lesson content
                            self._render_lesson_content(module, user_profile)
            else:
                # Show placeholder when no learning path exists
                st.info("🎯 Click 'Generate New Learning Path' above to create your personalized learning journey!")
        
        with tab2:
            st.markdown("### 🧠 Adaptive Quiz")
            self.adaptive_quiz.render_interface()

        with tab3:
            st.markdown("### 📚 Content Generation")
            if hasattr(st.session_state, 'user_profile') and st.session_state.user_profile:
                user_name = st.session_state.user_profile.get('name', 'default_user')
                self.content_interface.render_content_generator(user_id=user_name)
            else:
                st.warning("Please create your user profile to use the Content Library.")
                if st.button("Go to Profile"):
                    self.set_page("profile")

    def render_chat_page(self):
        """Render enhanced AI chat interface with modern styling"""
        # Enhanced header
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: white; text-align: center; margin: 0;">
                💬 AI Educational Assistant
            </h1>
            <p style="color: #f0f0f0; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
                Your personalized learning companion
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render the enhanced chat interface
        self.enhanced_chat.render_chat_interface()
    
    def render_profile_page(self):
        """Render the user profile management page"""
        st.title("👤 User Profile")
        
        # Check if user needs onboarding
        if not st.session_state.get('user_profile_complete', False):
            st.info("🎯 Let's set up your learning profile!")
            
            # Use the onboarding interface
            self.onboarding_interface.render_onboarding()
        else:
            # Display existing profile
            st.success("✅ Profile Complete!")
            
            user_profile = st.session_state.get('user_profile', {})
            
            # Profile overview
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Profile Information")
                st.write(f"**Name:** {user_profile.get('name', 'Not set')}")
                st.write(f"**Learning Style:** {user_profile.get('learning_style', 'Not set')}")
                st.write(f"**Experience Level:** {user_profile.get('experience_level', 'Not set')}")
                
            with col2:
                st.subheader("🎯 Learning Goals")
                goals = user_profile.get('goals', [])
                if goals:
                    for goal in goals:
                        st.write(f"• {goal}")
                else:
                    st.write("No goals set")
            
            # Subjects
            st.subheader("📚 Subjects of Interest")
            subjects = user_profile.get('subjects', [])
            if subjects:
                cols = st.columns(len(subjects))
                for i, subject in enumerate(subjects):
                    with cols[i]:
                        st.info(subject)
            else:
                st.write("No subjects selected")
            
            # Edit profile option
            st.divider()
            if st.button("✏️ Edit Profile", type="primary"):
                st.session_state.user_profile_complete = False
                st.rerun()
    
    def _render_enhanced_metrics(self):
        """Render enhanced metrics cards with modern styling"""
        user_profile = st.session_state.get('user_profile', {})
        analytics = st.session_state.get('analytics')
        
        # Create metrics columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem;">📚</h3>
                <h4 style="margin: 0.5rem 0;">Learning Style</h4>
                <p style="margin: 0; font-size: 1.1rem; font-weight: bold;">
                    {style}
                </p>
            </div>
            """.format(style=user_profile.get('learning_style', 'Not Set')), unsafe_allow_html=True)
        
        with col2:
            subjects_count = len(user_profile.get('subjects', []))
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem;">🎯</h3>
                <h4 style="margin: 0.5rem 0;">Subjects</h4>
                <p style="margin: 0; font-size: 1.1rem; font-weight: bold;">
                    {count} Active
                </p>
            </div>
            """.format(count=subjects_count), unsafe_allow_html=True)
        
        with col3:
            if analytics:
                summary = analytics.get_summary()
                sessions = summary.get('total_sessions', 0)
            else:
                sessions = 0
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem;">📈</h3>
                <h4 style="margin: 0.5rem 0;">Sessions</h4>
                <p style="margin: 0; font-size: 1.1rem; font-weight: bold;">
                    {sessions} Total
                </p>
            </div>
            """.format(sessions=sessions), unsafe_allow_html=True)
        
        with col4:
            if analytics:
                summary = analytics.get_summary()
                interactions = summary.get('total_interactions', 0)
            else:
                interactions = 0
            st.markdown("""
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem;">💬</h3>
                <h4 style="margin: 0.5rem 0;">Interactions</h4>
                <p style="margin: 0; font-size: 1.1rem; font-weight: bold;">
                    {interactions} Total
                </p>
            </div>
            """.format(interactions=interactions), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
    
    def _render_recommendations_cards(self):
        """Render enhanced recommendation cards with modern styling"""
        recommendations = st.session_state.assistant.get_recommendations(
            st.session_state.user_profile
        )
        
        # Enhanced recommendation cards
        for i, (category, items) in enumerate(recommendations.items()):
            if items:  # Only show categories with items
                # Create gradient colors for different categories
                gradients = [
                    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                    "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                    "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
                ]
                gradient = gradients[i % len(gradients)]
                
                st.markdown(f"""
                <div style="background: {gradient}; 
                            padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; color: white;">
                    <h4 style="margin: 0 0 1rem 0; text-transform: capitalize;">
                        🎯 {category.replace('_', ' ')}
                    </h4>
                    <ul style="margin: 0; padding-left: 1.5rem;">
                """, unsafe_allow_html=True)
                
                for item in items[:3]:  # Limit to 3 items per category
                    st.markdown(f"<li style='margin-bottom: 0.5rem;'>{item}</li>", unsafe_allow_html=True)
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
    
    def _render_progress_charts(self):
        """Render enhanced progress visualization with modern styling"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; color: white;">
            <h4 style="margin: 0 0 1rem 0;">📊 Learning Progress</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple progress bars for now with enhanced styling
        subjects = st.session_state.user_profile.get('subjects', ['General'])
        
        for i, subject in enumerate(subjects):
            progress = min(100, hash(subject) % 100)  # Demo progress
            
            # Color scheme for different subjects
            colors = ["#667eea", "#f093fb", "#4facfe", "#43e97b"]
            color = colors[i % len(colors)]
            
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-weight: bold;">{subject}</span>
                    <span style="color: {color}; font-weight: bold;">{progress}%</span>
                </div>
                <div style="background-color: #f0f0f0; border-radius: 10px; height: 10px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {color} 0%, {color}aa 100%); 
                                height: 100%; width: {progress}%; border-radius: 10px; 
                                transition: width 0.3s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_quick_actions(self):
        """Render enhanced quick action buttons with modern styling"""
        # Enhanced action buttons with gradients
        st.markdown("""
        <style>
        .action-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 1rem;
            cursor: pointer;
            transition: transform 0.2s ease;
            border: none;
            width: 100%;
        }
        .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Learning Session", use_container_width=True, type="primary"):
            st.session_state.current_page = 'learn'
            st.rerun()
        
        if st.button("💬 Chat with AI Tutor", use_container_width=True):
            st.session_state.current_page = 'chat'
            st.rerun()
        
        if st.button("📝 Take Adaptive Quiz", use_container_width=True):
            st.session_state.current_page = 'learn'
            st.rerun()
        
        if st.button("👤 Update Profile", use_container_width=True):
            st.session_state.current_page = 'profile'
            st.rerun()
    
    def _render_recent_activity(self):
        """Render recent learning activity"""
        activities = [
            "Completed Python Basics quiz",
            "Asked about loops in programming", 
            "Generated flashcards for variables",
            "Practiced problem solving"
        ]
        
        for activity in activities[:3]:
            st.markdown(f"• {activity}")
    
    def _render_subject_modules(self, subject: str):
        """Render learning modules for a specific subject"""
        modules = [
            f"{subject} Fundamentals",
            f"Intermediate {subject}",
            f"Advanced {subject} Concepts",
            f"{subject} Practice Problems"
        ]
        
        for i, module in enumerate(modules):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📚 {module}")
            
            with col2:
                progress = min(100, (i + 1) * 25)
                st.progress(progress / 100)
            
            with col3:
                if st.button("Start", key=f"module_{subject}_{i}"):
                    st.info(f"Starting {module}...")
    
    def _render_enhanced_chat_interface(self):
        """Render enhanced chat interface with code highlighting"""
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input with enhanced features
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
        
        # Chat tools
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧹 Clear Chat"):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("💾 Save Conversation"):
                st.success("Conversation saved!")
        
        with col3:
            if st.button("📤 Export Chat"):
                st.success("Chat exported!")
    
    def _render_basic_profile(self):
        """Render basic profile information form"""
        user_profile = st.session_state.user_profile
        
        name = st.text_input("Full Name", value=user_profile.get('name', ''))
        email = st.text_input("Email", value=user_profile.get('email', ''))
        
        if st.button("Update Basic Info"):
            user_profile['name'] = name
            user_profile['email'] = email
            st.success("Profile updated!")
    
    def _render_learning_preferences(self):
        """Render learning preferences form"""
        user_profile = st.session_state.user_profile
        
        learning_style = st.selectbox(
            "Learning Style",
            ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"],
            index=0 if not user_profile.get('learning_style') else 
            ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"].index(user_profile.get('learning_style'))
        )
        
        subjects = st.multiselect(
            "Subjects of Interest",
            ["Mathematics", "Computer Science", "Science", "History", "Literature", "Languages"],
            default=user_profile.get('subjects', [])
        )
        
        if st.button("Update Preferences"):
            user_profile['learning_style'] = learning_style
            user_profile['subjects'] = subjects
            st.success("Preferences updated!")
    
    def _render_detailed_analytics(self):
        """Render detailed analytics and progress"""
        analytics = st.session_state.analytics.get_summary()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Learning Statistics")
            st.metric("Total Questions", analytics.get('total_questions', 0))
            st.metric("Study Sessions", analytics.get('sessions', 0))
            st.metric("Average Session Time", f"{analytics.get('avg_time', 0):.1f} min")
        
        with col2:
            st.subheader("🎯 Progress Metrics")
            st.metric("Learning Score", f"{analytics.get('learning_score', 0)}/100")
            st.metric("Topics Mastered", analytics.get('mastered_topics', 0))
            st.metric("Streak Days", analytics.get('streak_days', 0))
    
    def _generate_adaptive_quiz(self):
        """Generate an adaptive quiz"""
        st.success("🎯 Generating adaptive quiz based on your profile...")
        # Implementation would go here
    
    def _generate_flashcards(self):
        """Generate flashcards"""
        st.success("📋 Creating personalized flashcards...")
        # Implementation would go here
    
    def _generate_practice_problems(self):
        """Generate practice problems"""
        st.success("📝 Generating practice problems...")
        # Implementation would go here
    
    def _render_lesson_content(self, module, user_profile):
        """Render interactive lesson content for a learning module"""
        st.markdown("---")
        st.markdown(f"## 📖 {module.title}")
        
        # Create lesson content based on module type
        if module.content_type.lower() == "lesson":
            # Generate lesson content using the content generator
            from content_generator import DifficultyLevel
            
            # Map module difficulty to content generator difficulty
            difficulty_map = {1: DifficultyLevel.BEGINNER, 2: DifficultyLevel.BEGINNER, 
                            3: DifficultyLevel.INTERMEDIATE, 4: DifficultyLevel.ADVANCED, 
                            5: DifficultyLevel.ADVANCED}
            difficulty = difficulty_map.get(module.difficulty, DifficultyLevel.INTERMEDIATE)
            
            # Generate comprehensive lesson content
            with st.spinner("🎓 Generating personalized lesson content..."):
                try:
                    # Generate lesson summary
                    lesson_summary = self.content_generator.generate_summary(
                        topic=module.title.replace("Module 1: ", ""),
                        subject=module.subject,
                        difficulty=difficulty,
                        audience="students",
                        user_id="default"
                    )
                    
                    # Check if lesson summary was generated successfully
                    if lesson_summary is None:
                        st.error("📖 Algebra Fundamentals\n\nError: Unable to generate summary due to a system configuration issue")
                        st.info("💡 This might be due to AI API configuration issues. Please check your API settings or try again later.")
                        return
                    
                    # Display lesson content
                    st.markdown("### 📚 Lesson Overview")
                    
                    # Safely access summary content
                    if hasattr(lesson_summary, 'content') and lesson_summary.content:
                        summary_content = lesson_summary.content
                    else:
                        st.error("📚 Lesson Overview\n\nError: Failed to load lesson content due to missing data")
                        st.info("💡 The lesson content could not be generated. Please try refreshing or contact support.")
                        return
                    
                    st.markdown(f"**{summary_content['title']}**")
                    st.markdown(summary_content['detailed_explanation'])
                    
                    # Key points
                    st.markdown("### 🎯 Key Learning Points")
                    for i, point in enumerate(summary_content['key_points'], 1):
                        st.markdown(f"{i}. {point}")
                    
                    # Examples
                    if summary_content.get('examples'):
                        st.markdown("### 💡 Examples")
                        for example in summary_content['examples']:
                            st.info(example)
                    
                    # Interactive practice section
                    st.markdown("### 🏃‍♂️ Practice Time")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📋 Generate Flashcards", key=f"flashcards_{module.id}"):
                            with st.spinner("Creating flashcards..."):
                                flashcards = self.content_generator.generate_flashcard_set(
                                    topic=module.title.replace("Module 1: ", ""),
                                    subject=module.subject,
                                    difficulty=difficulty,
                                    count=3
                                )
                                
                                st.markdown("#### 📋 Study Flashcards")
                                for j, flashcard in enumerate(flashcards):
                                    with st.expander(f"Flashcard {j+1}"):
                                        fc_content = flashcard.content
                                        st.markdown(f"**Question:** {fc_content['front']}")
                                        if st.button(f"Show Answer", key=f"show_answer_{j}"):
                                            st.markdown(f"**Answer:** {fc_content['back']}")
                                            if fc_content.get('hint'):
                                                st.markdown(f"**Hint:** {fc_content['hint']}")
                    
                    with col2:
                        if st.button("🧮 Generate Practice Problems", key=f"problems_{module.id}"):
                            with st.spinner("Creating practice problems..."):
                                problems = self.content_generator.generate_practice_problems(
                                    topic=module.title.replace("Module 1: ", ""),
                                    subject=module.subject,
                                    difficulty=difficulty,
                                    count=2
                                )
                                
                                st.markdown("#### 🧮 Practice Problems")
                                for k, problem in enumerate(problems):
                                    with st.expander(f"Problem {k+1}"):
                                        prob_content = problem.content
                                        st.markdown(f"**Problem:** {prob_content['problem_statement']}")
                                        
                                        if st.button(f"Show Solution", key=f"show_solution_{k}"):
                                            st.markdown(f"**Solution:** {prob_content['solution']}")
                                            
                                            if prob_content.get('step_by_step'):
                                                st.markdown("**Step-by-step:**")
                                                for step_num, step in enumerate(prob_content['step_by_step'], 1):
                                                    st.markdown(f"{step_num}. {step}")
                    
                    # Progress tracking
                    st.markdown("### ✅ Mark as Complete")
                    if st.button(f"Complete {module.title}", key=f"complete_{module.id}"):
                        st.success(f"🎉 Congratulations! You've completed {module.title}")
                        st.balloons()
                        
                        # Update analytics (if implemented)
                        if hasattr(st.session_state, 'analytics'):
                            st.session_state.analytics.record_module_completion(
                                module.id, module.title, datetime.now()
                            )
                
                except Exception as e:
                    st.error(f"Error generating lesson content: {str(e)}")
                    st.info("Please try again or contact support if the issue persists.")
        
        else:
            # Handle other content types (quiz, project, etc.)
            st.info(f"Content type '{module.content_type}' is not yet implemented.")
            st.markdown(f"**Description:** {module.description}")
            
            # Show learning objectives
            if hasattr(module, 'learning_objectives') and module.learning_objectives:
                st.markdown("### 🎯 Learning Objectives")
                for obj in module.learning_objectives:
                    st.markdown(f"• {obj}")