"""
Application Configuration and Environment Settings.

Use Case:
- Centralizes all environment configuration values, database credentials, security keys,
  AI provider settings, hybrid ranking weights, and CORS policies.
- Uses Pydantic BaseSettings for strict type validation and automatic `.env` file parsing.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings Model.

    Use Case:
    - Defines global configuration constants with fallback defaults.
    - Loaded across services, routes, and database connectors.
    """
    PROJECT_NAME: str = "KPi-Tech AI Food Ordering System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    DEBUG: bool = True

    # Security & JWT Configuration
    SECRET_KEY: str = "kpitech-ai-engineer-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours validity for authentication tokens

    # Database Configuration (Async SQLite default, easily swappable for PostgreSQL)
    DATABASE_URL: str = "sqlite+aiosqlite:///./food_ordering.db"

    # AI NLP Configuration
    AI_PROVIDER: str = "mock"  # 'mock' for deterministic local parsing or 'openai' for live LLM
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    AI_TIMEOUT_SECONDS: float = 3.5

    # Hybrid Search Scoring Weights (Weights sum to 1.0)
    # Use Case: Balances semantic relevance, keyword accuracy, dietary alignment, and popularity
    SEMANTIC_WEIGHT: float = 0.40
    KEYWORD_WEIGHT: float = 0.25
    PREFERENCE_WEIGHT: float = 0.20
    POPULARITY_WEIGHT: float = 0.15

    # Cross-Origin Resource Sharing (CORS) Allowed Origins for Frontend Integration
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


# Singleton instance accessible throughout the application
settings = Settings()
