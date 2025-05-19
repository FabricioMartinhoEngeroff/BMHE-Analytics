from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()

# URL do banco (exemplo com SQLite para desenvolvimento)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bmhe.db")

# ✅ Engine assíncrona
engine = create_async_engine(DATABASE_URL, echo=True)

# ✅ Criando sessão assíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ Declarative Base (compatível com SQLAlchemy 2.0+)
class Base(DeclarativeBase):
    pass
