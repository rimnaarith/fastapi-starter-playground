from fastapi import APIRouter
from .endpoints import auth, users, files

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(files.router, prefix="/files", tags=["Files"])