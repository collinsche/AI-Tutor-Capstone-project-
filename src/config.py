#!/usr/bin/env python3
"""
Configuration Module
Centralized configuration management for the AI Educational Assistant
"""

import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class AIConfig:
    """AI model configuration"""
    model_name: str = "x-ai/grok-4"
    max_tokens: int = 1000
    temperature: float = 0.7
    api_key: str = ""
    api_base_url: str = "https://openrouter.ai/api/v1"
    timeout: int = 30
    use_demo_mode: bool = True

@dataclass
class AppConfig:
    """Application configuration"""
    app_name: str = "AI Educational Assistant"
    version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    data_dir: str = "data"
    max_session_duration: int = 120  # minutes
    auto_save_interval: int = 300  # seconds

@dataclass
class LearningConfig:
    """Learning-specific configuration"""
    default_learning_style: str = "Visual"
    supported_subjects: list = None
    difficulty_levels: list = None
    max_recommendations: int = 10
    session_timeout: int = 1800  # seconds
    
    def __post_init__(self):
        if self.supported_subjects is None:
            self.supported_subjects = [
                "Mathematics", "Science", "History", "Literature", 
                "Computer Science", "Languages", "Arts", "Social Studies"
            ]
        
        if self.difficulty_levels is None:
            self.difficulty_levels = ["Beginner", "Intermediate", "Advanced"]

@dataclass
class UIConfig:
    """User interface configuration"""
    theme: str = "light"
    sidebar_width: int = 300
    chat_height: int = 400
    show_analytics: bool = True
    show_recommendations: bool = True
    max_chat_history: int = 100

class ConfigManager:
    """Configuration manager class"""
    
    def __init__(self):
        self.ai_config = AIConfig()
        self.app_config = AppConfig()
        self.learning_config = LearningConfig()
        self.ui_config = UIConfig()
        
        # Load from environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # AI Configuration
        self.ai_config.api_key = os.getenv("GROK_API_KEY", "")
        self.ai_config.model_name = os.getenv("AI_MODEL", self.ai_config.model_name)
        self.ai_config.temperature = float(os.getenv("AI_TEMPERATURE", self.ai_config.temperature))
        self.ai_config.api_base_url = os.getenv('AI_BASE_URL', self.ai_config.api_base_url)
        self.ai_config.max_tokens = int(os.getenv("AI_MAX_TOKENS", self.ai_config.max_tokens))
        self.ai_config.use_demo_mode = os.getenv("USE_DEMO_MODE", "false").lower() == "true"
        
        # App Configuration
        self.app_config.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.app_config.log_level = os.getenv("LOG_LEVEL", self.app_config.log_level)
        self.app_config.data_dir = os.getenv("DATA_DIR", self.app_config.data_dir)
        
        # UI Configuration
        self.ui_config.theme = os.getenv("UI_THEME", self.ui_config.theme)
    
    def get_ai_config(self) -> AIConfig:
        """Get AI configuration"""
        return self.ai_config
    
    def get_app_config(self) -> AppConfig:
        """Get application configuration"""
        return self.app_config
    
    def get_learning_config(self) -> LearningConfig:
        """Get learning configuration"""
        return self.learning_config
    
    def get_ui_config(self) -> UIConfig:
        """Get UI configuration"""
        return self.ui_config
    
    def update_config(self, config_type: str, **kwargs):
        """Update configuration values"""
        if config_type == "ai":
            for key, value in kwargs.items():
                if hasattr(self.ai_config, key):
                    setattr(self.ai_config, key, value)
        elif config_type == "app":
            for key, value in kwargs.items():
                if hasattr(self.app_config, key):
                    setattr(self.app_config, key, value)
        elif config_type == "learning":
            for key, value in kwargs.items():
                if hasattr(self.learning_config, key):
                    setattr(self.learning_config, key, value)
        elif config_type == "ui":
            for key, value in kwargs.items():
                if hasattr(self.ui_config, key):
                    setattr(self.ui_config, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert all configurations to dictionary"""
        return {
            "ai": self.ai_config.__dict__,
            "app": self.app_config.__dict__,
            "learning": self.learning_config.__dict__,
            "ui": self.ui_config.__dict__
        }
    
    def validate_config(self) -> Dict[str, list]:
        """Validate configuration and return any issues"""
        issues = {
            "errors": [],
            "warnings": []
        }
        
        # Validate AI config
        if not self.ai_config.api_key:
            issues["warnings"].append("Grok API key not set - using demo mode")
        
        if self.ai_config.temperature < 0 or self.ai_config.temperature > 2:
            issues["errors"].append("AI temperature must be between 0 and 2")
        
        if self.ai_config.max_tokens < 1 or self.ai_config.max_tokens > 4000:
            issues["warnings"].append("AI max_tokens should be between 1 and 4000")
        
        # Validate app config
        if not os.path.exists(self.app_config.data_dir):
            try:
                os.makedirs(self.app_config.data_dir, exist_ok=True)
            except Exception as e:
                issues["errors"].append(f"Cannot create data directory: {e}")
        
        # Validate learning config
        if self.learning_config.default_learning_style not in ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"]:
            issues["errors"].append("Invalid default learning style")
        
        return issues

# Global configuration instance
config = ConfigManager()

# Convenience functions
def get_ai_config() -> AIConfig:
    return config.get_ai_config()

def get_app_config() -> AppConfig:
    return config.get_app_config()

def get_learning_config() -> LearningConfig:
    return config.get_learning_config()

def get_ui_config() -> UIConfig:
    return config.get_ui_config()