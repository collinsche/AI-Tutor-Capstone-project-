import streamlit as st
import requests
import os


def render_learning_paths():
    st.markdown('<div class="dashboard-hero"><div class="abstract-shapes"><span class="shape mint"></span><span class="shape pink"></span><span class="shape purple"></span></div><h1>Design Your Learning Path</h1><p class="hero-subtitle">Pick a topic and we’ll choreograph a plan that fits your style.</p></div>', unsafe_allow_html=True)

    # Topic chips
    st.write("Suggested topics: ")
    chip_cols = st.columns(5)
    topics = ["Python Basics", "Data Science", "Web Dev", "Machine Learning", "Algorithms"]
    if 'lp_topic' not in st.session_state:
        st.session_state.lp_topic = ""

    for i, t in enumerate(topics):
        with chip_cols[i % 5]:
            if st.button(f"🔥 {t}", key=f"chip_{t}"):
                st.session_state.lp_topic = t
                st.rerun()

    topic = st.text_input("Enter a topic you want to learn about:", value=st.session_state.lp_topic)

    col1, col2 = st.columns([2,1])
    with col1:
        if st.button("✨ Generate Path"):
            if topic:
                with st.spinner("Generating your learning path..."):
                    try:
                        prompt = f"Create a 5-step, detailed learning path for a {st.session_state.user_profile.get('learning_style')} learner on the topic of {topic}. Each step should have a title, a short description, and a key learning objective."
                        api_url = "http://127.0.0.1:8000/generate"
                        # Quick connectivity check to backend docs
                        try:
                            if requests.get(api_url.replace('/generate', '/docs'), timeout=5).status_code != 200:
                                raise ConnectionError("Backend not reachable")
                        except Exception:
                            pass

                        response = requests.post(
                            api_url,
                            json={"prompt": prompt, "user_profile": st.session_state.user_profile},
                            timeout=30
                        )
                        response.raise_for_status()
                        learning_path = response.json().get('response', '')

                        st.header("Your Personalized Learning Path")
                        steps = learning_path.split('\n\n')
                        for i, step in enumerate(steps):
                            with st.expander(f"Step {i+1}"):
                                st.markdown(step)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error generating learning path: {e}")
            else:
                st.warning("Please enter a topic.")
    with col2:
        st.info("Tip: Use concise topics like 'Python Basics' or 'Linear Algebra'.")