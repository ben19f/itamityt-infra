from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        env_names={"database_url": "DATABASE_URL"}
    )

settings = Settings()
