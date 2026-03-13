# from pydantic_settings import BaseSettings, SettingsConfigDict
#
# class Settings(BaseSettings):
#     database_url: str
#
#     model_config = SettingsConfigDict(
#         env_names={"database_url": "DATABASE_URL"}, # связываем имя поля с переменной окружения
#         env_file="../.env",           # путь к .env-файлу
#         env_file_encoding="utf-8",   # кодировка файла
#         case_sensitive=False,         # регистронезависимый поиск переменных
#     )
#
# settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",  # путь к .env-файлу
        env_prefix="",  # без префикса
        env_names={"database_url": "DATABASE_URL"}  # связываем имя поля с переменной окружения
    )

settings = Settings()
