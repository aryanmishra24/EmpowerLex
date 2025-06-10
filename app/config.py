import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google Gemini API
    gemini_api_key: str = "AIzaSyC0pEMXFk2jW8YQhzKcuR49GrZzULZeHko"
    gemini_api_url: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    # OpenAI API (for fallback)
    openai_api_key: Optional[str] = None
    
    # Email (optional)
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # App
    app_name: str = "Legal Aid Platform"
    debug: bool = True
    cors_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()
