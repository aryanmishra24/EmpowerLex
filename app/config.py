import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./app.db"  # Default to SQLite for development
    )
    
    # PostgreSQL specific settings
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_user: str = os.getenv("POSTGRES_USER", "empowerlex")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
    postgres_db: str = os.getenv("POSTGRES_DB", "empowerlex")
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google Gemini API
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    gemini_api_url: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    # OpenAI API (for fallback)
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # App
    app_name: str = "Legal Aid Platform"
    debug: bool = True
    cors_origins: List[str] = ["*"]
    
    @property
    def postgres_url(self) -> str:
        """Generate PostgreSQL URL from components"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    class Config:
        env_file = ".env"

settings = Settings()
