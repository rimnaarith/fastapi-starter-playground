from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from app.modules.auth.service import AuthService, get_auth_service
from app.core.config import settings

from app.modules.auth.schemas import (
  LoginRequest,
  Platform,
  RefreshRequest, 
  TokenResponse, 
  UserRegister, 
  RegisterResponse
)

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
async def register(
  payload: UserRegister,
  service: AuthService = Depends(get_auth_service)
):
  return await service.register(payload)


@router.post("/login", response_model=TokenResponse, response_model_exclude_none=True)
async def login(
  payload: LoginRequest,
  response: Response,
  service: AuthService = Depends(get_auth_service)
):
  tokens = await service.login(email=payload.email, password=payload.password)

  if payload.platform == Platform.MOBILE:
    return tokens

  response.set_cookie(
    key="refresh_token",
    value=tokens.refresh_token,
    httponly=True,
    secure=True,          # False only for local HTTP development
    samesite="lax",       # or "strict"/"none" depending on frontend
    max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    path="/api/v1/auth",
  )

  return TokenResponse(
    access_token=tokens.access_token
  )
  

@router.post("/refresh", response_model=TokenResponse, response_model_exclude_none=True)
async def refresh_token(
  response: Response,
  payload: RefreshRequest | None = None,
  refresh_token_cookie: str | None = Cookie(default=None, alias="refresh_token"),
  service: AuthService = Depends(get_auth_service)
):
  
  refresh_token = refresh_token_cookie or (payload.refresh_token if payload else None)

  if not refresh_token:
    raise HTTPException(status_code=401, detail="Missing refresh token")
  
  tokens = await service.refresh_token(refresh_token)

  # If request is from mobile
  if refresh_token_cookie is None:
    return tokens
  
  # If request is from web → set cookie
  response.set_cookie(
    key="refresh_token",
    value=tokens.refresh_token,
    httponly=True,
    secure=True,          # False only for local HTTP development
    samesite="lax",       # or "strict"/"none" depending on frontend
    max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    path="/api/v1/auth",
  )

  return TokenResponse(
    access_token=tokens.access_token
  )