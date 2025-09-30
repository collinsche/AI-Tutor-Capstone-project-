import streamlit as st
from onboarding import render_onboarding
from dashboard import render_dashboard
from chat import render_chat
from learning_paths import render_learning_paths
from quiz import render_quiz
from dotenv import load_dotenv
import os

load_dotenv()

# Debugging: Print the API key to verify it's loaded
print(f"OPENROUTER_API_KEY: {os.getenv("OPENROUTER_API_KEY")}")

def main():
    # Set page configuration as the VERY FIRST Streamlit command
    st.set_page_config(
        page_title="AI Learning Assistant",
        page_icon="🎓",
        layout="wide"
    )

    # Load the consolidated CSS file
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Error: style.css not found. Please ensure it is in the same directory.")
        return

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'onboarding'
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    if 'lp_topic' not in st.session_state:
        st.session_state.lp_topic = ""
    if 'dashboard_stats' not in st.session_state:
        st.session_state.dashboard_stats = {
            'questions_today': 16,
            'study_streak': 3,
            'topics_mastered': 4,
            'learning_score': 83,
        }
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar navigation
    st.sidebar.title("Navigation")
    if st.session_state.onboarding_complete:
        page_options = {
            "Dashboard": "dashboard",
            "Chat": "chat",
            "Learning Paths": "learn",
            "Quiz": "quiz"
        }
        current_key = next((k for k, v in page_options.items() if v == st.session_state.page), "Dashboard")
        selection = st.sidebar.radio("Go to", list(page_options.keys()), index=list(page_options.keys()).index(current_key))
        if st.session_state.page != page_options[selection]:
            st.session_state.page = page_options[selection]
            st.rerun()
    else:
        st.session_state.page = 'onboarding'

    # Page routing
    if st.session_state.page == 'onboarding':
        render_onboarding()
    elif st.session_state.page == 'dashboard':
        render_dashboard()
    elif st.session_state.page == 'chat':
        render_chat()
    elif st.session_state.page == 'learn':
        render_learning_paths()
    elif st.session_state.page == 'quiz':
        render_quiz()

if __name__ == "__main__":
    main()