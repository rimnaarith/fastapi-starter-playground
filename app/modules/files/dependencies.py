from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.files.repository import FileRepository
from app.modules.files.service import FileService
from app.shared.storage.factory import get_storage
from app.shared.storage.interface import Storage


def get_file_repository(db: AsyncSession = Depends(get_db)):
  return FileRepository(db)


def get_file_service(file_repo: FileRepository = Depends(get_file_repository), storage: Storage = Depends(get_storage)):
  return FileService(file_repo, storage)