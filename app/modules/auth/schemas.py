from enum import StrEnum

from pydantic import BaseModel, EmailStr

class Platform(StrEnum):
  WEB = "web"
  MOBILE = "mobile"

class UserRegister(BaseModel):
  firstname: str
  lastname: str
  email: EmailStr
  password: str

class RegisterResponse(BaseModel):
  id: str
  email: EmailStr

  class Config:
    from_attributes = True


class LoginRequest(BaseModel):
  email: EmailStr
  password: str
  platform: Platform

class TokenResponse(BaseModel):
  access_token: str
  refresh_token: str | None = None
  token_type: str = "Bearer"