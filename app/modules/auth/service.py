from fastapi import Depends

from app.core.security import hash_password
from app.modules.auth.schemas import UserRegister, RegisterResponse
from app.modules.users.service import UserService, get_user_service


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

def get_auth_service(
  user_service: UserService = Depends(get_user_service),
):
  return AuthService(user_service)