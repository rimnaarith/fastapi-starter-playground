from fastapi import APIRouter, Depends

from .service import AuthService, get_auth_service

from .schemas import UserRegister, RegisterResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=RegisterResponse)
async def create_user(
  payload: UserRegister,
  service: AuthService = Depends(get_auth_service)
):
  return await service.register(payload)