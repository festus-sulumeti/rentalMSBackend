from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from extensions import db
import models  # noqa: F401 - loads every model into SQLAlchemy metadata
from config import database_uri

# Alembic Config object
config = context.config

config.set_main_option("sqlalchemy.url", database_uri())

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your SQLAlchemy metadata here later
# Example:
# from app import db
# target_metadata = db.metadata

target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

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
    """Run migrations in online mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
