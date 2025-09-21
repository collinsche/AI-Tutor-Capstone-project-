#!/usr/bin/env python3
"""
Generative AI Personalized Educational Assistant
Main application entry point with enhanced routing and UI
"""

import streamlit as st
from dotenv import load_dotenv   # 1. Import the function
from app_router import AppRouter

load_dotenv()  # 2. Load variables from .env file

def main():
    """Main application function with routing"""
    # Initialize and run the application router
    router = AppRouter()
    router.run()

if __name__ == "__main__":
    main()