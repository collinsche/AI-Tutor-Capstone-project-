from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import requests
import os
from dotenv import load_dotenv
import json

# FastAPI Application
app = FastAPI(
    title="AI Companion API",
    description="API for AI Companion application, providing chat and content generation services.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request and response
class GenerateRequest(BaseModel):
    prompt: str
    user_profile: dict = Field(default_factory=dict)

class GenerateResponse(BaseModel):
    response: str

class QuizGenerateRequest(BaseModel):
    user_profile: dict = Field(default_factory=dict)



class QuizGenerateResponse(BaseModel):
    quiz_questions: list[dict]

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Generates text based on a given prompt and user profile using the OpenRouter API.
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not set")

    enhanced_prompt = f"User Profile: {request.user_profile}. Based on this, {request.prompt}"

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "x-ai/grok-4-fast:free",
                "messages": [{"role": "user", "content": enhanced_prompt}]
            }
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        generated_text = result['choices'][0]['message']['content']
        return GenerateResponse(response=generated_text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"OpenRouter API request failed: {e}")
    except KeyError:
        raise HTTPException(status_code=500, detail="Failed to parse API response")

@app.post("/generate_quiz", response_model=QuizGenerateResponse)
async def generate_quiz(request: GenerateRequest):
    """
    Generates quiz questions based on a given user profile using the OpenRouter API.
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not set")

    user_profile = request.user_profile
    interests = user_profile.get("subjects", ["general knowledge"])
    learning_style = user_profile.get("learning_style", "any")
    experience_level = user_profile.get("experience_level", "beginner")

    # Craft a more detailed prompt for quiz generation
    quiz_prompt = f"Generate 5 multiple-choice quiz questions for a {experience_level} level learner with a {learning_style} learning style, focusing on the following topics: {', '.join(interests)}. Each question should have 4 options and indicate the correct answer. Format the output as a JSON array of objects, where each object has 'q' (question), 'options' (a list of strings), 'answer' (the correct option string), 'interest' (one of the specified topics), and 'explain' (a brief explanation of the correct answer)."

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "x-ai/grok-4-fast:free",
                "messages": [{"role": "user", "content": quiz_prompt}]
            }
        )
        response.raise_for_status()
        result = response.json()
        generated_text = result['choices'][0]['message']['content']
        
        # Attempt to parse the generated text as JSON
        try:
            quiz_data = json.loads(generated_text)
            # Validate the structure of each question
            for q in quiz_data:
                if not all(key in q for key in ["q", "options", "answer", "interest"]):
                    raise ValueError("Missing keys in quiz question object")
                if not isinstance(q["options"], list) or len(q["options"]) != 4:
                    raise ValueError("Options must be a list of 4 strings")
            return {"quiz_questions": quiz_data}
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse or validate quiz questions from API response: {e}. Response was: {generated_text}")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"OpenRouter API request failed: {e}")
    except KeyError:
        raise HTTPException(status_code=500, detail="Failed to parse API response for quiz generation")