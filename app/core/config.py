import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "أبو رامي AI"

    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-3.8-flash"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    vOPENROUTER_MODEL: str = "google/gemini-2.0-flash-exp:free"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    DATABASE_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"

    APP_VERSION: str = "1.0.0"

    def get_database_url(self) -> str:
        url = (self.DATABASE_URL or "").strip()
        if not url:
            return "sqlite+aiosqlite:////tmp/abu_rami.db"
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
