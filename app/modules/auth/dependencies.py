from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.core.security import decode_token
from app.modules.auth.service import AuthService
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService
from app.modules.users.dependencies import get_user_repository, get_user_service


bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service(
  user_service: UserService = Depends(get_user_service),
):
  return AuthService(user_service)


async def get_current_user(
  credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
  user_repo: UserRepository = Depends(get_user_repository),
) -> User:
  if credentials is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Authentication required",
    )
  
  token = credentials.credentials

  try:
    payload = decode_token(token)
  except JWTError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid access token",
    )
  
  if payload.get("type") != "access":
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token type",
    )
  
  user_id = payload.get("sub")

  if user_id is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token payload",
    )
  
  user = await user_repo.get_by_id(UUID(user_id))

  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User not found",
    )
  
  return user