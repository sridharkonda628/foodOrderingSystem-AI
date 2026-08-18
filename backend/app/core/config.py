from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "KPi-Tech AI Food Ordering System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "kpitech-ai-engineer-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./food_ordering.db"

    # AI Configuration
    AI_PROVIDER: str = "mock"  # 'mock' or 'openai'
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    AI_TIMEOUT_SECONDS: float = 3.5

    # Hybrid Search Weights
    SEMANTIC_WEIGHT: float = 0.40
    KEYWORD_WEIGHT: float = 0.25
    PREFERENCE_WEIGHT: float = 0.20
    POPULARITY_WEIGHT: float = 0.15

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
