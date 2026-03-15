import sys
import os

# добавляем app/ в путь
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from logging.config import fileConfig
from sqlalchemy import create_engine, pool  # <- используем синхронный движок
from alembic import context

from core.config import settings      # т.к. теперь sys.path включает app/
from db.base import Base
from models import user, item

target_metadata = Base.metadata

# Alembic Config
config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using a synchronous engine."""
    # создаем **синхронн**
