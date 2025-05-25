import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# 1) Carrega variáveis do .env
load_dotenv()

# 2) Lê a URL assincrona e converte em síncrona
raw_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bmhe.db")
sync_url = raw_url.replace("+aiosqlite", "")  # ex.: "sqlite:///./bmhe.db"

# 3) Adiciona a raiz do projeto ao sys.path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
)

# 4) Importa o metadata central (via registry)
from mcp_backend.app.config.database import registry  # noqa: E402

# 5) Configura o objeto Alembic
config = context.config

# 6) Configura o log do Alembic, se existir arquivo de config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 7) Define o metadata alvo para autogenerate
target_metadata = registry.metadata

# 8) Seta a URL SÍNCRONA no config do Alembic
config.set_main_option("sqlalchemy.url", sync_url)

def run_migrations_offline():
    """Executa migrações em modo offline."""
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
    """Executa migrações em modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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

# 9) Escolhe o modo de execução
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
