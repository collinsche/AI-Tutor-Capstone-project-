import streamlit as st
import datetime
import pandas as pd
import os

def render_dashboard():
    # Dynamic greeting based on time, name, and avatar
    now = datetime.datetime.now()
    if now.hour < 12:
        greeting = "Good morning"
    elif now.hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    user_name = st.session_state.user_profile.get('name', 'Learner')
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png"},
        "owl": {"image": "images/owl.png"},
        "cat": {"image": "images/cat.png"}
    }
    st.markdown('<div class="dashboard-hero"><div class="abstract-shapes"><span class="shape mint"></span><span class="shape pink"></span><span class="shape purple"></span></div>', unsafe_allow_html=True)
    if os.path.exists(avatar_data[avatar]["image"]):
        st.image(avatar_data[avatar]["image"], width=50, use_container_width=False, clamp=True)  # Updated parameter
    else:
        st.write("[Avatar Missing]")
    st.markdown(f'<h1>{greeting}, {user_name}! 🌟</h1><p class="hero-subtitle">Ready to continue your learning journey?</p></div>', unsafe_allow_html=True)

    # Stats metrics with icons
    if 'dashboard_stats' not in st.session_state:
        st.session_state.dashboard_stats = {
            'questions_today': 16,
            'study_streak': 3,
            'topics_mastered': 4,
            'learning_score': 83,
        }
    stats = st.session_state.dashboard_stats

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<i class="fas fa-question-circle icon-metric"></i>', unsafe_allow_html=True)
        st.metric("Questions Today", stats['questions_today'], delta=-1)
    with col2:
        st.markdown('<i class="fas fa-fire icon-metric"></i>', unsafe_allow_html=True)
        st.metric("Study Streak", f"{stats['study_streak']} days", delta=1)
    with col3:
        st.markdown('<i class="fas fa-trophy icon-metric"></i>', unsafe_allow_html=True)
        st.metric("Topics Mastered", stats['topics_mastered'], delta=0)
    with col4:
        st.markdown('<i class="fas fa-chart-line icon-metric"></i>', unsafe_allow_html=True)
        st.metric("Learning Score", f"{stats['learning_score']}/100", delta=6)

    # Progress Overview
    st.subheader("📈 Progress Overview")
    progress_col1, progress_col2 = st.columns(2)
    with progress_col1:
        st.write("Weekly Learning Progress")
        weekly_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Hours': [2, 3, 1, 4, 2, 5, 0]
        })
        st.bar_chart(weekly_data, x='Day', y='Hours', color="#9B5DE5")
    with progress_col2:
        st.write("Subject Progress")
        interests = st.session_state.user_profile.get('subjects', ['Python', 'Mathematics'])
        for subject in interests:
            progress = 25 if subject == 'Python' else 50
            st.progress(progress / 100)
            st.write(f"{subject}: {progress}%")

    # Personalized Recommendations
    st.subheader("📚 Recommended for You")
    interests = st.session_state.user_profile.get('subjects', [])
    if interests:
        st.write(f"Based on your interests in {', '.join(interests)}:")
        for interest in interests:
            st.write(f" - Explore advanced {interest} topics or try a quiz!")
    else:
        st.write("Complete onboarding to get personalized recommendations.")

    # Quick Actions
    st.subheader("⚡ Quick Actions")
    st.markdown('<div class="quick-grid">', unsafe_allow_html=True)
    qa_col1, qa_col2, qa_col3 = st.columns(3)
    with qa_col1:
        st.markdown('<div class="quick-card"><h3 class="quick-title">Learning Page</h3><p class="quick-desc">Explore lessons tailored for you.</p></div>', unsafe_allow_html=True)
        if st.button("Go to Learning ➜"):
            st.session_state.page = 'learn'
            st.rerun()
    with qa_col2:
        st.markdown('<div class="quick-card"><h3 class="quick-title">Quiz</h3><p class="quick-desc">Challenge yourself and track progress.</p></div>', unsafe_allow_html=True)
        if st.button("Start a Quiz ➜"):
            st.session_state.page = 'quiz'
            st.rerun()
    with qa_col3:
        st.markdown('<div class="quick-card"><h3 class="quick-title">AI Tools</h3><p class="quick-desc">Use AI helpers for explanations and practice.</p></div>', unsafe_allow_html=True)
        if st.button("Open AI Tools ➜"):
            st.session_state.page = 'chat'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Recent Activity with st.image()
    st.subheader("🕒 Recent Activity")
    activities = [
        {"icon": "📝", "title": "Python Basics Quiz", "type": "Quiz • 19:42", "score": "Score: 85%"},
        {"icon": "💬", "title": "Asked about loops", "type": "Chat • 16:42", "score": ""},
        {"icon": "📚", "title": "Completed Variables lesson", "type": "Module • 21:42", "score": "Score: 92%"},
        {"icon": "💻", "title": "Coding exercises", "type": "Practice • 21:42", "score": "Score: 78%"},
    ]
    for act in activities:
        if os.path.exists(avatar_data[avatar]["image"]):
            st.image(avatar_data[avatar]["image"], width=30, use_container_width=False)  # Updated parameter
        else:
            st.write("[Avatar Missing]")
        st.markdown(f'<div class="activity-item">{act["icon"]} <strong>{act["title"]}</strong> <br> {act["type"]} {act["score"]}</div>', unsafe_allow_html=True)

    # Achievements & Badges
    st.subheader("Achievements & Badges")
    if 'badge_count' not in st.session_state:
        st.session_state.badge_count = 0
    st.write(f"You have {st.session_state.badge_count} badges. Keep going!")
    if st.button("Claim a Badge 🎉"):
        st.session_state.badge_count += 1
        st.balloons()
        st.success("Badge claimed!")