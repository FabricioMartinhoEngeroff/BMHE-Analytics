import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Importa o metadata central (via registry)
from mcp_backend.app.config.database import registry 

# Configura o objeto Alembic
config = context.config

# Configura o log do alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o metadata alvo para autogenerate
target_metadata = registry.metadata

# Define a URL do banco a partir do .env
config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bmhe.db")
)

def run_migrations_offline():
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
