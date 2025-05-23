from typing import AsyncGenerator

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bmhe.db")

# ✅ Engine assíncrona para uso na aplicação
engine_async = create_async_engine(DATABASE_URL, echo=True)

# ✅ Engine síncrona para Alembic
engine_sync = create_engine(DATABASE_URL.replace("+aiosqlite", ""), echo=True)

# ✅ Sessão assíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
 async with AsyncSessionLocal() as session:
        yield session

# ✅ Base declarativa (comum para sync e async)
class Base(DeclarativeBase):
    pass

# ✅ Registry para integração com Alembic
registry = Base.registry
