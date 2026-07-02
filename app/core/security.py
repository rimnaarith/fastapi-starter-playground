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