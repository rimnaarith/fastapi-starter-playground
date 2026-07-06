from fastapi import Depends

from app.modules.auth.service import AuthService
from app.modules.users.service import UserService
from app.modules.users.dependencies import get_user_service


def get_auth_service(
  user_service: UserService = Depends(get_user_service),
):
  return AuthService(user_service)