from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db

from .models import User

class UserRepository:
  def __init__(self, db: AsyncSession):
    self.db = db

  async def create( self, firstname: str, lastname: str, email: str, password: str):
    user = User(
      firstname=firstname,
      lastname=lastname,
      email=email,
      password=password
    )

    self.db.add(user)
    await self.db.commit()
    await self.db.refresh(user)

    return user

  async def get_by_email(self, email: str):
    result = await self.db.execute(
      select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()
  
def get_user_repository(db: AsyncSession = Depends(get_db)):
  return UserRepository(db)