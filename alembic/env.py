from __future__ import annotations

import os
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config object
config = context.config

# Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# Ensure project root is on sys.path (so imports work)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import app metadata and DB URL
from app.db.base import Base  # DeclarativeBase
from app.core.config import DATABASE_URL

# Import models so they are registered on Base.metadata
# (important for autogenerate to see them)
import app.models.user  # noqa: F401
import app.models.task  # noqa: F401

target_metadata = Base.metadata


def _to_sync_url(url: str) -> str:
    """
    Convert an async SQLAlchemy URL to a sync one for Alembic.
    """
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    # psycopg is already sync by default
    return url


def get_url() -> str:
    # Prefer app config; fallback to alembic.ini if not set
    url = os.getenv("DATABASE_URL", DATABASE_URL)
    return _to_sync_url(url)


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """
    # Inject URL dynamically
    alembic_cfg = config.get_section(config.config_ini_section) or {}
    alembic_cfg["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        alembic_cfg,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()