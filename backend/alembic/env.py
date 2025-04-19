import asyncio
from logging.config import fileConfig
import os
from pathlib import Path # Import Path
from dotenv import load_dotenv # Keep load_dotenv
from urllib.parse import urlparse, parse_qs # Import URL parsing utilities

# from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine

from alembic import context

# Import Base from your models base file
from app.models.base import Base
# # Import your application's settings (should now have loaded .env)
# from app.core.config import settings # Bypassing settings object here

# Determine the project root relative to this script file
# env.py is in backend/alembic/, so root is three levels up
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOTENV_PATH = PROJECT_ROOT / ".env"

# Load .env file from the calculated project root
if DOTENV_PATH.is_file():
    load_dotenv(dotenv_path=DOTENV_PATH)
else:
    print(f"Warning: .env file not found at {DOTENV_PATH}")

# Explicitly get DATABASE_URL from environment AFTER loading .env
# Ensure it includes the +asyncpg driver type
DATABASE_URL_FOR_ALEMBIC = os.getenv("DATABASE_URL")
if not DATABASE_URL_FOR_ALEMBIC:
    raise ValueError("DATABASE_URL not found in environment after loading .env")
if not DATABASE_URL_FOR_ALEMBIC.startswith("postgresql+asyncpg://"):
    print("Warning: DATABASE_URL in .env does not start with postgresql+asyncpg://")
    # Optionally, attempt to fix it (use with caution)
    if DATABASE_URL_FOR_ALEMBIC.startswith("postgresql://"):
        DATABASE_URL_FOR_ALEMBIC = DATABASE_URL_FOR_ALEMBIC.replace("postgresql://", "postgresql+asyncpg://", 1)
        print("Attempted to prefix DATABASE_URL with +asyncpg")
    else:
        raise ValueError("DATABASE_URL in .env does not seem to be a valid postgresql URL")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the database URL from the explicitly loaded environment variable
config.set_main_option("sqlalchemy.url", DATABASE_URL_FOR_ALEMBIC)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Directly use the URL loaded from environment
    context.configure(
        url=DATABASE_URL_FOR_ALEMBIC, # Use explicitly loaded URL
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Parse the URL to check for sslmode
    parsed_url = urlparse(DATABASE_URL_FOR_ALEMBIC)
    query_params = parse_qs(parsed_url.query)
    ssl_mode = query_params.get('sslmode', [None])[0]

    connect_args = {}
    if ssl_mode == 'require':
        # If sslmode=require, pass ssl=True to asyncpg
        connect_args["ssl"] = True

    # Create engine with explicit connect_args if needed
    connectable = create_async_engine(
        DATABASE_URL_FOR_ALEMBIC,
        poolclass=pool.NullPool,
        connect_args=connect_args  # Pass ssl=True if required
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # run_migrations_online()
    asyncio.run(run_migrations_online())
