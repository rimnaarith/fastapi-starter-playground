from fastapi import HTTPException
from .repository import UserRepository


class UserService:
  def __init__(self, repo: UserRepository):
    self.repo = repo

  async def create_user(self, name: str, email: str):
    # prevent duplicate email
    existing = await self.repo.get_by_email(email)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return await self.repo.create(name, email)