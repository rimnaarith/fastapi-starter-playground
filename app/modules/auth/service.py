from fastapi import Depends, HTTPException

from app.core.security import (
  decode_token,
  hash_password,
  verify_password,
  create_access_token,
  create_refresh_token,
)
from app.modules.auth.schemas import UserRegister, RegisterResponse
from app.modules.users.service import UserService, get_user_service

from .schemas import TokenResponse


class AuthService:
  def __init__(self, user_service: UserService):
    self.user_service = user_service
  
  async def register(self, user: UserRegister) -> RegisterResponse:
    hashed_password = hash_password(user.password)
    new_user = await self.user_service.create_user(
      firstname=user.firstname,
      lastname=user.lastname,
      email=user.email,
      hashed_password=hashed_password
    )
    return RegisterResponse(
      id=str(new_user.id),
      email=new_user.email
    )
  
  async def login(self, email: str, password: str):
    user = await self.user_service.get_by_email(email)

    if not user:
      raise HTTPException(401)
    
    if not verify_password(password, user.password):
      raise HTTPException(401)
    
    return TokenResponse(
      access_token=create_access_token(str(user.id)),
      refresh_token=create_refresh_token(str(user.id))
    )

  async def refresh_token(self, refresh_token: str):
    try:
      payload = decode_token(refresh_token)
    except Exception:
      raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
      raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = payload.get("sub")
    user = await self.user_service.get_by_id(user_id)

    if not user:
      raise HTTPException(status_code=401, detail="User not found")
    
    return TokenResponse(
      access_token=create_access_token(str(user.id)),
      refresh_token=create_refresh_token(str(user.id))
    )

def get_auth_service(
  user_service: UserService = Depends(get_user_service),
):
  return AuthService(user_service)