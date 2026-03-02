from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Agent Info
    AGENT_VERSION: str = "1.0.0"
    AGENT_PORT: int = 8000
    DEBUG: bool = False
    
    # CI/CD Platforms
    GITHUB_TOKEN: Optional[str] = None
    GITLAB_TOKEN: Optional[str] = None
    JENKINS_URL: Optional[str] = None
    JENKINS_USER: Optional[str] = None
    JENKINS_TOKEN: Optional[str] = None
    
    # AI Configuration
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-4"
    AI_PROVIDER: str = "openai"  # openai, ollama, anthropic, groq, gemini
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Agent Behavior
    POLLING_INTERVAL: int = 30
    AUTO_FIX_ENABLED: bool = True
    AUTO_COMMIT_ENABLED: bool = True
    MAX_RETRY_ATTEMPTS: int = 3
    
    # Database
    DATABASE_URL: str = "sqlite:///./agent.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "agent.log"
    
    # Dashboard (optional, not used by backend)
    DASHBOARD_PORT: Optional[int] = None
    API_BASE_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields

settings = Settings()
