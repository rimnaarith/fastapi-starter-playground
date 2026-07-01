from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from .repository import UserRepository
from .service import UserService
from .schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


def get_service(db: AsyncSession = Depends(get_db)):
  repo = UserRepository(db)
  return UserService(repo)


@router.post("/", response_model=UserResponse)
async def create_user(
  payload: UserCreate,
  service: UserService = Depends(get_service)
):
  return await service.create_user(
    payload.username,
    payload.email
  )