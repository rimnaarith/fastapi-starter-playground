from pydantic import BaseModel, EmailStr

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