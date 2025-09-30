# AI Learning Assistant

## Overview
The AI Learning Assistant is an interactive application designed to provide personalized learning experiences. It features an onboarding process to tailor content to user preferences, a dashboard to track progress, a chat interface for AI interaction, dynamic learning paths, and an adaptive quiz system.

## Features
- **Personalized Onboarding**: Gathers user preferences (avatar, name, learning style, experience level, reasoning, subjects) to customize the learning experience.
- **Interactive Dashboard**: Displays learning statistics, progress overview, personalized recommendations, quick actions, and recent activity.
- **AI Tutor Chat**: A chat interface powered by an AI model to answer questions and provide explanations.
- **Dynamic Learning Paths**: Generates customized learning paths based on user-selected topics and profiles.
- **Adaptive Quiz System**: Creates quizzes with multiple-choice questions, provides instant feedback, and explanations for incorrect answers.

## Architecture
The application consists of two main components:
1.  **Frontend (Streamlit)**: Built with Streamlit, this part handles the user interface, user interactions, and displays content. It communicates with the FastAPI backend for AI-powered functionalities.
2.  **Backend (FastAPI)**: A FastAPI application that exposes API endpoints for:
    *   `/generate`: Generates text responses based on prompts and user profiles using the OpenRouter API.
    *   `/generate_quiz`: Generates quiz questions with explanations based on user profiles and specified topics using the OpenRouter API.

## Setup Instructions

### Prerequisites
- Python 3.8+
- `pip` (Python package installer)

### 1. Clone the Repository
```bash
git clone <repository_url>
cd Cap
```

### 2. Set up Environment Variables
Create a `.env` file in the root directory of the project and add your OpenRouter API key:
```
OPENROUTER_API_KEY="your_openrouter_api_key_here"
```
Replace `"your_openrouter_api_key_here"` with your actual OpenRouter API key.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Backend
Open a terminal and navigate to the project root directory. Run the FastAPI backend:
```bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```
The backend will be running at `http://0.0.0.0:8000`.

### 5. Run the Frontend
Open another terminal and navigate to the project root directory. Run the Streamlit frontend:
```bash
python3 -m streamlit run main.py
```
The Streamlit application will open in your browser, usually at `http://localhost:8501`.

## Known Issues and Fixes
-   **`KeyError: 'generated_text'` in Learning Paths and Chat**:
    *   **Issue**: The frontend was expecting a key named `'generated_text'` from the backend's `/generate` endpoint, but the backend was returning `'response'`.
    *   **Fix**: Modified `learning_paths.py` and `chat.py` to correctly parse the response using `response.json()['response']`.
-   **`422 Client Error` in Quiz Generation**:
    *   **Issue**: The `/generate_quiz` endpoint in `api.py` expected a `prompt` field in the request body, which was missing from the frontend's request.
    *   **Fix**: Updated `quiz.py` to include a `prompt` field in the JSON payload sent to the `/generate_quiz` endpoint.
-   **`KeyError: 'explain'` in Quiz Section**:
    *   **Issue**: The quiz frontend (`quiz.py`) was attempting to display an explanation using the `'explain'` key, but the backend's quiz generation prompt was not explicitly asking the AI to include this field.
    *   **Fix**: Modified the `quiz_prompt` in `api.py` to explicitly request an `'explain'` field for each question.
-   **Duplicate Explanation Display in Quiz**:
    *   **Issue**: A duplicate line for displaying the explanation was present in `quiz.py`, leading to redundant output.
    *   **Fix**: Removed the redundant line in `quiz.py`.

## Future Enhancements
-   Implement automated end-to-end testing.
-   Conduct a more thorough AI integration validation with mock tests and simulated API failures.
-   Add more robust error handling and user feedback mechanisms.
-   Expand the range of AI models and customization options.
-   Implement user authentication and persistent data storage.