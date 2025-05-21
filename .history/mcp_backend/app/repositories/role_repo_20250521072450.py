from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from mcp_backend.app.domain.models.role import Role

class RoleRepository:

    async def find_by_name(self, db: AsyncSession, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        result = await db.scalars(stmt)
        return result.first()