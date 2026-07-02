Since you're already experienced with Express.js, TypeScript, and scalable frontend architectures, I'd recommend structuring a FastAPI project more like a backend service than a simple script. A feature-based structure scales much better than organizing everything by file type.

## Recommended Project Structure

```
app/
├── api/
│   ├── deps.py
│   ├── v1/
│   │   ├── api.py
│   │   ├── users.py
│   │   ├── auth.py
│   │   └── posts.py
│   └── v2/
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── database.py
│   ├── logging.py
│   └── exceptions.py
│
├── models/
│   ├── user.py
│   ├── post.py
│   └── __init__.py
│
├── schemas/
│   ├── user.py
│   ├── auth.py
│   └── post.py
│
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   └── post_service.py
│
├── repositories/
│   ├── user_repository.py
│   ├── post_repository.py
│   └── base.py
│
├── middleware/
│   ├── auth.py
│   ├── request_logger.py
│   └── cors.py
│
├── utils/
│   ├── jwt.py
│   ├── email.py
│   ├── pagination.py
│   └── helpers.py
│
├── tasks/
│   ├── emails.py
│   └── cleanup.py
│
├── static/
├── templates/
│
├── main.py
└── __init__.py

tests/
├── api/
├── services/
├── repositories/
└── conftest.py

alembic/

.env
.env.example
requirements.txt
pyproject.toml
README.md
```

---

# Even Better: Feature-Based Architecture

For larger applications, organize by feature instead of layer.

```
app/
├── api/
│   ├── v1/
│   │   ├── router.py
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── blog.py
│   │   │   └── comments.py
│   │
│   ├── v2/
│   │   ├── router.py
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── ...
│
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
│
├── modules/
│   ├── auth/
│   │   ├── service.py
│   │   ├── repository.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── dependencies.py
│   │
│   ├── users/
│   │   ├── service.py
│   │   ├── repository.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── blog/
│   ├── comments/
│   └── upload/
│
├── shared/
│   ├── pagination.py
│   ├── exceptions.py
│   ├── responses.py
│   └── utils.py
│
└── main.py
```

This keeps everything related to a feature together.

---

## Typical Request Flow

```
Client
   │
   ▼
Router
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
Database
```

Example:

```
POST /login
        │
        ▼
router.py
        │
        ▼
auth_service.py
        │
        ▼
user_repository.py
        │
        ▼
SQLAlchemy
```

---

# Responsibility of Each Layer

### Router

Only HTTP-related code.

```python
@router.post("/login")
async def login(
    data: LoginRequest,
    service: AuthService = Depends()
):
    return await service.login(data)
```

No business logic.

---

### Service

Business rules.

```python
class AuthService:

    async def login(self, data):
        user = await self.repo.find_by_email(data.email)

        if not user:
            raise InvalidCredential()

        if not verify_password(data.password, user.password):
            raise InvalidCredential()

        return create_token(user)
```

---

### Repository

Database only.

```python
class UserRepository:

    async def find_by_email(self, email):
        return await self.session.scalar(
            select(User).where(User.email == email)
        )
```

No validation.

No JWT.

No permissions.

---

### Schema

Validation.

```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

---

### Model

Database model.

```python
class User(Base):
    __tablename__ = "users"

    id = mapped_column(primary_key=True)
    email = mapped_column(String)
```

---

# Dependency Injection

FastAPI makes this simple.

```python
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
```

```python
class UserRepository:
    def __init__(self, db=Depends(get_db)):
        self.db = db
```

```python
class UserService:
    def __init__(self, repo=Depends(UserRepository)):
        self.repo = repo
```

---

# Configuration

```
core/
    config.py
```

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    DEBUG: bool = False

settings = Settings()
```

---

# Database

```
core/database.py
```

```python
engine = create_async_engine(...)

AsyncSessionLocal = async_sessionmaker(engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

---

# Error Handling

Centralize exceptions.

```python
@app.exception_handler(NotFoundException)
async def handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )
```

---

# Authentication

```
modules/
    auth/
        router.py
        service.py
        jwt.py
```

Avoid putting JWT logic in routers.

---

# Testing

Mirror your application structure.

```
tests/
    auth/
    users/
    blog/
```

Test services independently from the API.

---

# Useful Libraries

| Purpose               | Library                                           |
| --------------------- | ------------------------------------------------- |
| ORM                   | SQLAlchemy 2.0 (Async)                            |
| Migration             | Alembic                                           |
| Validation            | Pydantic v2                                       |
| Authentication        | python-jose or PyJWT                              |
| Password hashing      | pwdlib or passlib (if compatible with your stack) |
| Background tasks      | Celery, Dramatiq, or FastAPI `BackgroundTasks`    |
| Dependency Injection  | FastAPI `Depends`                                 |
| Environment variables | pydantic-settings                                 |
| Testing               | pytest + httpx                                    |
| Logging               | Loguru or the standard `logging` module           |

## Best Practices

* Keep routers thin; move business logic into services.
* Keep repositories focused on data access only.
* Use asynchronous database access (`AsyncSession`) where appropriate.
* Validate all input with Pydantic models.
* Store configuration in environment variables and load it through `pydantic-settings`.
* Use Alembic for database migrations from the beginning.
* Prefer feature-based organization for medium and large projects.
* Write unit tests for services and integration tests for API endpoints.
* Add type hints throughout the codebase to improve readability and editor support.

Given your background with Express.js, this layered approach (`Router → Service → Repository → Database`) combined with feature-based modules will feel familiar and scales well as the application grows.
