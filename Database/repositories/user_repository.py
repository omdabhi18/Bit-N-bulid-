from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.models.user import User
from Database.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        res = await self.session.execute(select(User).filter(User.email == email))
        return res.scalars().first()

    async def find_by_email(self, email: str) -> Optional[User]:
        return await self.get_by_email(email)

    async def list_by_role(self, role: Any) -> list[User]:
        role_val = role.value if hasattr(role, "value") else str(role)
        res = await self.session.execute(select(User).filter(User.role == role_val))
        return list(res.scalars().all())

    async def get_by_phone(self, phone: str) -> Optional[User]:
        res = await self.session.execute(select(User).filter(User.phone == phone))
        return res.scalars().first()

