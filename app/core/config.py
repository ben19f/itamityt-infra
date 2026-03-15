from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",  # путь к .env-файлу
        env_prefix="",  # без префикса
        # env_file_encoding="utf-8",
        env_names={"database_url": "DATABASE_URL"}  # связываем имя поля с переменной окружения
    )

settings = Settings()
