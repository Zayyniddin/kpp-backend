# kpp/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = Field("KPP Backend", description="Название приложения")
    API_PREFIX: str = Field("/api")

    # PostgreSQL
    POSTGRES_USER: str = Field(..., description="PostgreSQL user")           # ← без дефолта
    POSTGRES_PASSWORD: str = Field(..., description="PostgreSQL password")   # ← без дефолта
    POSTGRES_DB: str = Field(..., description="Database name")               # ← без дефолта
    POSTGRES_HOST: str = Field("db", description="Database hostname")        # ← с дефолтом, ок для Docker
    POSTGRES_PORT: int = Field(5432, description="Database port")

    # Telegram
    TELEGRAM_BOT_TOKEN: str = Field(..., description="BotFather token")

    # Security
    SECRET_KEY: str = Field(..., description="JWT Secret")

    class Config:
        env_file = ".env"

settings = Settings()