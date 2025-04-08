from typing import Literal

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    DATABASE_URL: str
    TEST_DB_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_TRANSPORT: Literal["COOKIE", "BEARER"] = "COOKIE"

    # Настройки загрузки файлов
    IMAGES_DIR: str = "src/static/images/posts"
    URL_IMAGES_PREFIX: str = "images/posts"  # Часть URL после /static/
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/gif"]
    MAX_IMAGE_SIZE: int = Field(default=5 * 1024 * 1024, description="5MB limit")

    # Google oath
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def images_upload_path(self) -> Path:
        """Возвращает полный путь к директории для загрузки изображений"""
        path = BASE_DIR / self.IMAGES_DIR
        path.mkdir(parents=True, exist_ok=True)  # Создаем директорию если не существует
        return path



settings = Settings()
