from uuid import UUID

from fastapi import HTTPException

from app.modules.users.models import User
from .repository import UserRepository


class UserService:
  def __init__(self, repo: UserRepository):
    self.repo = repo

  async def create_user(self, firstname: str, lastname: str, email: str, hashed_password: str) -> User:
    # prevent duplicate email
    existing = await self.repo.get_by_email(email)

    if existing:
      raise HTTPException(
        status_code=400,
        detail="Email already exists"
      )
    return await self.repo.create(
      firstname=firstname,
      lastname=lastname,
      email=email,
      password=hashed_password
    )


  async def get_by_email(self, email: str):
    return await self.repo.get_by_email(email)
  

  async def get_by_id(self, id: str):
    return await self.repo.get_by_id(UUID(id))