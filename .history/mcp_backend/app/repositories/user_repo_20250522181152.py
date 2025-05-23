from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from mcp_backend.app.domain.models.user import User

class UserRepository:

    async def find_by_id(self, db: AsyncSession, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await db.scalars(stmt)
        return result.first()

    async def find_by_email(self, db: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await db.scalars(stmt)
        return result.first()

    async def exist_by_email(self, db: AsyncSession, email: str) -> bool:
        stmt = select(User).where(User.email == email)
        result = await db.scalars(stmt)
        return result.first() is not None

    async def exist_by_cpf(self, db: AsyncSession, cpf: str) -> bool:
        stmt = select(User).where(User.cpf == cpf)
        result = await db.scalars(stmt)
        return result.first() is not None

    async def save(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def delete(self, db: AsyncSession, user: User) -> None:
        await db.delete(user)
        await db.commit()
