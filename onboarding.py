import streamlit as st
import textwrap

def render_onboarding():
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False

    _render_stepper()
    if st.session_state.onboarding_step == 1:
        _render_avatar_step()
    elif st.session_state.onboarding_step == 2:
        _render_name_step()
    elif st.session_state.onboarding_step == 3:
        _render_learning_style_step()
    elif st.session_state.onboarding_step == 4:
        _render_level_step()
    elif st.session_state.onboarding_step == 5:
        _render_reasoning_step()
    elif st.session_state.onboarding_step == 6:
        _render_subjects_step()
    elif st.session_state.onboarding_step == 7:
        _render_complete_step()

def _render_stepper():
    steps = ["Avatar", "Name", "Learning Style", "Level", "Reasoning", "Subjects", "Complete"]
    current = st.session_state.onboarding_step
    progress = (current - 1) / (len(steps) - 1) * 100  # Adjust for complete step as final
    
    items = []
    for i, name in enumerate(steps):
        step_num = i + 1
        is_completed = step_num < current
        is_current = step_num == current
        step_class = "completed" if is_completed else "current" if is_current else ""
        progress_class = "active" if is_completed or is_current else ""
        
        item_html = textwrap.dedent(f'''
            <div class="step-item {step_class}">
                <div class="progress-ring-container">
                    <svg class="progress-ring">
                        <defs>
                            <linearGradient id="grad{step_num}" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#00d4ff" />
                                <stop offset="100%" stop-color="#ff006b" />
                            </linearGradient>
                        </defs>
                        <circle class="progress-ring-circle progress-ring-background" fill="none" stroke-width="3" r="18" cx="20" cy="20"></circle>
                        <circle class="progress-ring-circle progress-ring-progress {progress_class}" stroke="url(#grad{step_num})" fill="none" stroke-width="3" r="18" cx="20" cy="20"></circle>
                    </svg>
                    <div class="progress-ring-number">{step_num}</div>
                </div>
                <div class="step-label">{name}</div>
            </div>
        ''')
        items.append(item_html)

    stepper_html = f'<div class="stepper-container">{"".join(items)}</div>'
    progress_html = f'<div class="progress-rail"><div class="progress-fill" style="width: {progress}%;"></div></div><p class="progress-text">Progress: {int(progress)}%</p>'
    st.markdown(stepper_html + progress_html, unsafe_allow_html=True)
    st.write(" ")

def _render_avatar_step():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png", "message": "Beep boop! Pick me as your Robot guide!"},
        "owl": {"image": "images/owl.png", "message": "Hoo-hoo! Choose me as your Owl mentor!"},
        "cat": {"image": "images/cat.png", "message": "Meow! Select me as your Cat companion!"}
    }
    st.image(avatar_data[avatar]["image"], caption=f"Your AI Guide: {avatar.capitalize()}", width=100)
    st.write(avatar_data[avatar]["message"])
    st.title("Choose your AI Guide!")
    avatar_options = ["robot", "owl", "cat"]
    selected_avatar = st.radio("Select your AI avatar:", avatar_options, index=avatar_options.index(avatar), horizontal=True)
    if st.button("Next ➜"):
        if selected_avatar:
            st.session_state.user_profile['avatar'] = selected_avatar
            st.session_state.onboarding_step += 1
            st.rerun()

def _render_name_step():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png", "message": "Beep boop! I'm your Robot guide. What’s your name?"},
        "owl": {"image": "images/owl.png", "message": "Hoo's there? I'm your Owl mentor. What’s your name?"},
        "cat": {"image": "images/cat.png", "message": "Meow! I'm your Cat companion. What’s your name?"}
    }
    st.image(avatar_data[avatar]["image"], caption=f"Your AI Guide: {avatar.capitalize()}", width=100)
    st.write(avatar_data[avatar]["message"])
    st.title("Welcome! What should we call you?")
    name = st.text_input("Your Name", key="user_name", placeholder="Enter your name")
    if st.button("Next ➜"):
        if name:
            st.session_state.user_profile['name'] = name
            st.session_state.onboarding_step += 1
            st.rerun()

def _render_learning_style_step():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png", "message": "Nice to meet you! I'm your Robot guide. How do you learn best?"},
        "owl": {"image": "images/owl.png", "message": "Hoo-hoo! I'm your Owl mentor. How do you learn best?"},
        "cat": {"image": "images/cat.png", "message": "Purr-fect! I'm your Cat companion. How do you learn best?"}
    }
    st.image(avatar_data[avatar]["image"], caption=f"Your AI Guide: {avatar.capitalize()}", width=100)
    st.write(avatar_data[avatar]["message"])
    st.title(f"How do you learn best, {st.session_state.user_profile.get('name', 'friend')}?")
    options = ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"]
    selection = st.radio("Select a learning style:", options, horizontal=True)
    if st.button("Next ➜"):
        if selection:
            st.session_state.user_profile['learning_style'] = selection
            st.session_state.onboarding_step += 1
            st.rerun()

def _render_level_step():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png", "message": "Great choice! I'm your Robot guide. What’s your experience level?"},
        "owl": {"image": "images/owl.png", "message": "Wise choice! I'm your Owl mentor. What’s your experience level?"},
        "cat": {"image": "images/cat.png", "message": "Pawsome! I'm your Cat companion. What’s your experience level?"}
    }
    st.image(avatar_data[avatar]["image"], caption=f"Your AI Guide: {avatar.capitalize()}", width=100)
    st.write(avatar_data[avatar]["message"])
    st.title(f"What's your current experience level, {st.session_state.user_profile.get('name', 'friend')}?")
    level_labels = {1: "🌱 Beginner", 2: "📚 Basic Knowledge", 3: "⚡ Intermediate", 4: "🚀 Advanced"}
    level = st.select_slider("Drag to select your level", options=list(level_labels.keys()), value=2, format_func=lambda x: level_labels[x])
    if st.button("Next ➜"):
        if level:
            st.session_state.user_profile['level'] = level_labels[level]
            st.session_state.onboarding_step += 1
            st.rerun()

def _render_reasoning_step():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png", "message": "Interesting! I'm your Robot guide. Why are you learning?"},
        "owl": {"image": "images/owl.png", "message": "Intriguing! I'm your Owl mentor. Why are you learning?"},
        "cat": {"image": "images/cat.png", "message": "Curious! I'm your Cat companion. Why are you learning?"}
    }
    st.image(avatar_data[avatar]["image"], caption=f"Your AI Guide: {avatar.capitalize()}", width=100)
    st.write(avatar_data[avatar]["message"])
    st.title(f"Why are you learning, {st.session_state.user_profile.get('name', 'friend')}?")
    reasoning = st.text_input("Primary Motivation", key="reasoning", placeholder="e.g., Career growth, Curiosity")
    if st.button("Next ➜"):
        if reasoning:
            st.session_state.user_profile['reasoning'] = reasoning
            st.session_state.onboarding_step += 1
            st.rerun()

def _render_subjects_step():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png", "message": "Almost there! I'm your Robot guide. Pick your subjects!"},
        "owl": {"image": "images/owl.png", "message": "Nearly done! I'm your Owl mentor. Pick your subjects!"},
        "cat": {"image": "images/cat.png", "message": "Just a few more steps! I'm your Cat companion. Pick your subjects!"}
    }
    st.image(avatar_data[avatar]["image"], caption=f"Your AI Guide: {avatar.capitalize()}", width=100)
    st.write(avatar_data[avatar]["message"])
    st.title(f"Which subjects interest you, {st.session_state.user_profile.get('name', 'friend')}?")
    subjects = st.multiselect("Choose options", ["Python", "Mathematics", "Data Science", "Computer Science"])
    if st.button("Next ➜"):
        if subjects:
            st.session_state.user_profile['subjects'] = subjects
            st.session_state.onboarding_step += 1
            st.rerun()

def _render_complete_step():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png", "message": "Setup complete! I'm your Robot guide. Let's learn!"},
        "owl": {"image": "images/owl.png", "message": "All set! I'm your Owl mentor. Let's learn!"},
        "cat": {"image": "images/cat.png", "message": "Meow-tstanding! I'm your Cat companion. Let's learn!"}
    }
    st.image(avatar_data[avatar]["image"], caption=f"Your AI Guide: {avatar.capitalize()}", width=100)
    st.write(avatar_data[avatar]["message"])
    st.title(f"Welcome, {st.session_state.user_profile.get('name', 'friend')}! 🎉")
    st.write("Your profile is set. Click below to explore your dashboard.")
    if st.button("Go to Dashboard ➜"):
        st.session_state.onboarding_complete = True
        st.session_state.page = 'dashboard'
        st.balloons()  # Confetti effect
        st.rerun()

if __name__ == "__main__":
    render_onboarding()