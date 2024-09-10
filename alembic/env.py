import os
from sqlalchemy import create_engine, pool
from logging.config import fileConfig
from alembic import context

from app.models.star_wars_character_model import StarWarsCharacter
from database import Base

# Import your SQLAlchemy Base (where your models are defined)
# Alembic Config object, which provides access to the .ini file values
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Load the database URL from environment variables
database_url = os.getenv("DATABASE_URL")

# Override the `sqlalchemy.url` in Alembic's config with the environment variable
config.set_main_option("sqlalchemy.url", database_url)

# Metadata of your models, which Alembic will use to generate migrations
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
