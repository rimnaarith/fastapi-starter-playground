from datetime import UTC, datetime, timedelta

from jose import jwt
from .config import settings
from pwdlib import PasswordHash

# Create a password hasher using the recommended algorithm (Argon2)
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
  """
  Hash a plain text password.

  Example:
    "myPassword123"
    -> "$argon2id$v=19$m=65536,t=3,p=4$..."
  """
  return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
  """
  Verify a plain text password against its hash.
  """
  return password_hash.verify(password, hashed_password)



def create_access_token(subject: str):

  expire = datetime.now(UTC) + timedelta(
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
  )

  payload = {
    "sub": subject,
    "exp": expire,
    "type": "access",
  }

  return jwt.encode(
    payload,
    settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
  )


def create_refresh_token(subject: str):

  expire = datetime.now(UTC) + timedelta(
    days=settings.REFRESH_TOKEN_EXPIRE_DAYS
  )

  payload = {
    "sub": subject,
    "exp": expire,
    "type": "refresh",
  }

  return jwt.encode(
    payload,
    settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
  )


def decode_token(token: str):
  return jwt.decode(
    token,
    settings.SECRET_KEY,
    algorithms=[settings.ALGORITHM],
  )