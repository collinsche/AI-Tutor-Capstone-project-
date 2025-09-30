import streamlit as st
import requests
import os

def render_chat():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png"},
        "owl": {"image": "images/owl.png"},
        "cat": {"image": "images/cat.png"}
    }
    user_avatar = "images/user.png"  # Default user avatar path

    st.title("AI Tutor Chat")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            avatar_path = avatar_data[avatar]["image"] if message["role"] == "assistant" else user_avatar
            if os.path.exists(avatar_path):
                st.image(avatar_path, width=40, use_container_width=False)  # Updated parameter
            else:
                st.write(f"[{message['role'].capitalize()} Avatar Missing]")
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            if os.path.exists(user_avatar):
                st.image(user_avatar, width=40, use_container_width=False)  # Updated parameter
            else:
                st.write("[User Avatar Missing]")
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if os.path.exists(avatar_data[avatar]["image"]):
                st.image(avatar_data[avatar]["image"], width=40, use_container_width=False)  # Updated parameter
            else:
                st.write("[Assistant Avatar Missing]")
            with st.spinner("Thinking..."):
                try:
                    enhanced_prompt = f"{prompt}. User profile: learning style - {st.session_state.user_profile.get('learning_style', 'unknown')}, level - {st.session_state.user_profile.get('level', 'unknown')}"
                    api_url = "http://127.0.0.1:8000/generate"
                    # Quick connectivity check to backend docs
                    try:
                        if requests.get(api_url.replace('/generate', '/docs'), timeout=5).status_code != 200:
                            raise ConnectionError("Backend not reachable")
                    except Exception:
                        pass  # Continue; backend may still be reachable

                    response = requests.post(
                        api_url,
                        json={"prompt": enhanced_prompt, "user_profile": st.session_state.user_profile},
                        timeout=30
                    )
                    response.raise_for_status()
                    ai_response = response.json().get('response', '')
                    st.markdown(ai_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                except requests.exceptions.RequestException as e:
                    st.error(f"Error communicating with the backend: {e}")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()