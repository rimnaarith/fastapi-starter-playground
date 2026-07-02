from fastapi import APIRouter, Depends

from app.modules.auth.service import AuthService, get_auth_service

from app.modules.auth.schemas import UserRegister, RegisterResponse

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
async def create_user(
  payload: UserRegister,
  service: AuthService = Depends(get_auth_service)
):
  return await service.register(payload)