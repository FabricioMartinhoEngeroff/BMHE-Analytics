import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import AsyncGenerator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bmhe.db")

# Engine assíncrona (usar no app)
engine_async = create_async_engine(DATABASE_URL, echo=True)

# Engine **síncrona** (usar no Alembic e onde precisar de sync)
engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""), echo=True)

# Sessão assíncrona para FastAPI
AsyncSessionLocal = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Base declarativa
class Base(DeclarativeBase):
    pass

# Registry p/ Alembic
registry = Base.registry
