from __future__ import with_statement
from app.config import settings
from app.db import Base
import sys
from pathlib import Path
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# asegurarse de que 'app' esté en sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# importa models y metadata DESPUÉS de ajustar el path
import app.models  # noqa: F401

# objeto de configuración de alembic (NO sobrescribir con import)
config = context.config

# convertir url async a sync si es necesario
raw_url = str(settings.DATABASE_URL)
if "+asyncpg" in raw_url:
    database_url = raw_url.replace("+asyncpg", "")
else:
    database_url = raw_url

config.set_main_option("sqlalchemy.url", database_url)

# configurar logging desde alembic.ini si existe
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
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


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
