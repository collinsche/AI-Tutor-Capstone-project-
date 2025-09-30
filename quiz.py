import streamlit as st
import random
import requests
import json
import os
import pandas as pd
import datetime
import qrcode
import io
from PIL import Image, ImageDraw, ImageFont
import time
import uuid

# Static fallback questions
QUESTIONS = [
    {"q": "Which of the following is a Python data structure best for key-value pairs?", "options": ["List", "Tuple", "Dictionary", "Set"], "answer": "Dictionary", "explain": "Dictionaries store mappings of keys to values and are ideal for lookups.", "interest": "Python"},
    {"q": "What does len([1,2,3]) return?", "options": ["2", "3", "[1,2,3]", "TypeError"], "answer": "3", "explain": "len(...) returns the number of elements in the list, which is 3 here.", "interest": "Python"},
    {"q": "In Big-O notation, which has better average time complexity for search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "answer": "O(log n)", "explain": "Binary search on a sorted array achieves O(log n) average complexity.", "interest": "Algorithms"},
]

def generate_certificate(name, score, total):
    img = Image.new('RGB', (400, 200), color='gold')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()  # Customize font if needed
    draw.text((50, 50), f"Certificate for {name}", fill='black', font=font)
    draw.text((50, 100), f"Score: {score}/{total}", fill='black', font=font)
    img.save('certificate.png')
    return 'certificate.png'

def generate_ai_question(interest, level, previous_mistake=None):
    """Generate AI question using Grok 4 Fast via OpenRouter API."""
    base_prompt = f"Generate a {level} level quiz question on {interest} with exactly 4 options (A, B, C, D), correct answer, and explanation. Format: Q: [question] Options: A) [opt1] B) [opt2] C) [opt3] D) [opt4] Answer: [answer] Explain: [explanation]"
    if previous_mistake and st.session_state.get('quiz_mode') == "Challenge":
        # Radical twist: Trickier question based on mistake
        base_prompt += f" Make it trickier based on this previous mistake: {previous_mistake}. Add a subtle hint to guide without spoiling."
    api_url = "http://127.0.0.1:8000/generate"  # Your FastAPI endpoint
    try:
        # Debug: Test connection first
        test_response = requests.get(api_url.replace('/generate', '/docs'), timeout=5)
        if test_response.status_code != 200:
            raise ConnectionError("Backend not reachable")
        
        response = requests.post(
            api_url,
            json={"prompt": base_prompt, "user_profile": st.session_state.user_profile},
            timeout=30  # Increased timeout to 30 seconds
        )
        response.raise_for_status()
        api_response = response.json()
        # st.write("Sending request with prompt:", base_prompt)  # Uncomment for debug
        # st.write("Received API Response:", api_response)  # Uncomment for debug
        ai_q = api_response.get('response', '').strip()  # Use 'response' key and strip whitespace
        if not ai_q:
            raise ValueError("No valid response from AI")
        # Robust parsing
        parts = [p.strip() for p in ai_q.split("Options:") if p.strip()]
        if len(parts) < 2:
            raise ValueError("Invalid response format: Missing Options section")
        question = parts[0].replace("Q:", "").strip()
        options_part = parts[1].split("Answer:")[0].strip()
        options = [opt.strip() for opt in options_part.split(")")[1:] if opt.strip()]  # Extract A/B/C/D
        answer_part = parts[1].split("Answer:")[1].split("Explain:")[0].strip()
        explain = parts[1].split("Explain:")[1].strip() if len(parts[1].split("Explain:")) > 1 else "No explanation provided."
        if len(options) != 4:
            raise ValueError("Invalid options count")
        return {"q": question, "options": options, "answer": answer_part, "explain": explain, "interest": interest}
    except Exception as e:
        st.error(f"AI question generation failed: {e}. Using fallback.")
        return random.choice(QUESTIONS)  # Fallback to static

def render_quiz():
    avatar = st.session_state.user_profile.get('avatar', 'robot')
    avatar_data = {
        "robot": {"image": "images/robot.png", "encouragement": "Beep boop! Great job!"},
        "owl": {"image": "images/owl.png", "encouragement": "Hoo-hoo! Wise choice!"},
        "cat": {"image": "images/cat.png", "encouragement": "Purr-fect answer!"}
    }

    # Initialize session state (resets on "Play Again" for demo)
    if 'quiz_mode' not in st.session_state:
        st.session_state.quiz_mode = None
    if 'quiz_level' not in st.session_state:
        st.session_state.quiz_level = None
    if 'quiz_session_id' not in st.session_state:
        st.session_state.quiz_session_id = str(uuid.uuid4())[:8]
    if 'multiplayer_scores' not in st.session_state:
        st.session_state.multiplayer_scores = {}  # {player_name: score} - Demo-only, resets on rerun
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'previous_mistakes' not in st.session_state:
        st.session_state.previous_mistakes = []
    if 'timer_end' not in st.session_state:
        st.session_state.timer_end = None

    # Bold and Fun Header
    st.markdown('<div class="dashboard-hero"><div class="abstract-shapes"><span class="shape mint"></span><span class="shape pink"></span><span class="shape purple"></span></div><h1>Pop Quiz! 🚀</h1><p class="hero-subtitle">Get ready for an epic challenge!</p></div>', unsafe_allow_html=True)

    # Mode Selection
    if st.session_state.quiz_mode is None:
        st.subheader("🎮 Choose Your Adventure!")
        col_mode1, col_mode2 = st.columns(2)
        with col_mode1:
            if st.button("🧑 Solo Mode", type="primary"):
                st.session_state.quiz_mode = "Solo"
                st.session_state.multiplayer_scores = {}
                st.rerun()
        with col_mode2:
            if st.button("👥 Challenge Mode", type="primary"):
                st.session_state.quiz_mode = "Challenge"
                st.session_state.multiplayer_scores = {}
                st.rerun()
        return

    # Level Selection
    if st.session_state.quiz_level is None:
        st.subheader("📊 Pick Your Difficulty!")
        level = st.radio("Level:", ["Beginner (1 min)", "Intermediate (45 sec)", "Pro (30 sec)"], horizontal=True, key="level_select")
        if st.button("Start Quiz! 🎉", type="primary"):
            st.session_state.quiz_level = level
            st.session_state.current_question = 0
            st.session_state.quiz_score = 0
            st.session_state.previous_mistakes = []
            st.session_state.multiplayer_scores[st.session_state.user_profile.get('name', 'Player')] = 0
            st.rerun()
        return

    # Share Link/QR for Challenge Mode (Demo-Only, No Persistent Storage)
    if st.session_state.quiz_mode == "Challenge" and st.session_state.current_question == 0:
        st.subheader("👥 Invite Your Crew!")
        share_link = f"http://localhost:8501/quiz?session={st.session_state.quiz_session_id}"  # Local demo link
        st.write(f"**Share Link:** {share_link}")
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(share_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # Convert PIL Image to bytes for Streamlit
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.image(byte_im, caption="Scan to Join (Demo Mode)!", width=150, use_container_width=False)

    # Timer Setup
    time_limits = {"Beginner": 60, "Intermediate": 45, "Pro": 30}
    level_key = st.session_state.quiz_level.split()[0]
    timer_sec = time_limits.get(level_key, 60)
    if st.session_state.timer_end is None or st.session_state.current_question > 0:
        st.session_state.timer_end = time.time() + timer_sec

    # Progress Bar (Capped at 3 questions)
    max_questions = 3
    progress = min(st.session_state.current_question, max_questions) / max_questions * 100
    st.markdown(f'<div class="progress-rail"><div class="progress-fill" style="width:{progress}%"></div></div><p class="progress-text">Progress: {int(progress)}%</p>', unsafe_allow_html=True)

    # Timer Display
    time_left = max(0, st.session_state.timer_end - time.time())
    st.warning(f"⏱️ Time Left: {int(time_left)}s")
    if time_left <= 0:
        st.error("Time's up! Next question...")
        st.session_state.current_question = min(st.session_state.current_question + 1, max_questions)
        st.session_state.timer_end = time.time() + timer_sec
        st.rerun()

    # Multiplayer Leaderboard (Demo-Only, Resets on Rerun)
    if st.session_state.quiz_mode == "Challenge":
        st.subheader("🏆 Live Leaderboard")
        player_name = st.text_input("Enter your name to join:", value=st.session_state.user_profile.get('name', 'Player'), key="player_name")
        if player_name not in st.session_state.multiplayer_scores and st.button("Join Challenge!"):
            st.session_state.multiplayer_scores[player_name] = 0
            st.rerun()
        if st.session_state.multiplayer_scores:
            df = pd.DataFrame(list(st.session_state.multiplayer_scores.items()), columns=["Player", "Score"])
            st.dataframe(df.sort_values("Score", ascending=False))

    # Dynamic AI-Generated Question
    interests = st.session_state.user_profile.get('subjects', ['Python'])  # From onboarding
    previous_mistake = st.session_state.previous_mistakes[-1] if st.session_state.previous_mistakes else None
    q = generate_ai_question(interests[0], level_key, previous_mistake)

    st.subheader(f"Question {min(st.session_state.current_question + 1, max_questions)} of {max_questions}")
    st.write(f"**{q['q']}**")  # Bold for fun
    choice = st.radio("Your Answer:", q["options"], key=f"quiz_choice_{st.session_state.current_question}", horizontal=True)

    # Ensure player_name is defined (fallback for Solo or unset cases)
    player_name = st.session_state.user_profile.get('name', 'Anonymous') if 'player_name' not in locals() else player_name

    if st.button("Submit! 🔥", type="primary"):
        if choice == q["answer"]:
            st.success("Correct! 🎉")
            st.session_state.quiz_score += 1
            if os.path.exists(avatar_data[avatar]["image"]):
                st.image(avatar_data[avatar]["image"], width=50, use_container_width=False)
            st.write(avatar_data[avatar]["encouragement"])
        else:
            st.error("Oops! Try again!")
            st.info(f"**Explanation:** {q['explain']}")
            st.session_state.previous_mistakes.append(f"Answered '{choice}' for '{q['q']}' when correct was '{q['answer']}'")
        st.session_state.multiplayer_scores[player_name] = st.session_state.quiz_score if player_name in st.session_state.multiplayer_scores else 0
        st.session_state.current_question = min(st.session_state.current_question + 1, max_questions)  # Cap at max_questions
        st.session_state.timer_end = time.time() + timer_sec
        st.rerun()

    # Quiz Complete
    if st.session_state.current_question >= max_questions:
        st.subheader("Quiz Complete! 🎊")
        score = st.session_state.quiz_score
        total = max_questions
        st.write(f"**You scored {score} / {total} ({int(score/total*100)}%)**")
        st.balloons()
        
        # Update Leaderboard
        if st.session_state.quiz_mode == "Challenge":
            df = pd.DataFrame(list(st.session_state.multiplayer_scores.items()), columns=["Player", "Score"])
            st.dataframe(df.sort_values("Score", ascending=False))

        # Certificate
        if st.button("Download Certificate! 🏅"):
            cert_path = generate_certificate(st.session_state.user_profile.get('name', 'Player'), score, total)
            with open(cert_path, "rb") as f:
                st.download_button("Download", f, file_name="quiz_certificate.png")

        if st.button("Play Again! 🔄"):
            st.session_state.quiz_mode = None
            st.session_state.quiz_level = None
            st.session_state.current_question = 0
            st.session_state.quiz_score = 0
            st.session_state.previous_mistakes = []
            st.session_state.timer_end = None
            st.session_state.multiplayer_scores = {}  # Reset for demo
            st.rerun()

if __name__ == "__main__":
    render_quiz()