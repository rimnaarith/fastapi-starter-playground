
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService


def get_user_repository(db: AsyncSession = Depends(get_db)):
  return UserRepository(db)


def get_user_service(
  user_repo: UserRepository = Depends(get_user_repository),
):
  return UserService(user_repo)