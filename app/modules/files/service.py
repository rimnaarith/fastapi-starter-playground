from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status

from app.modules.files.models import File
from app.modules.files.repository import FileRepository
from app.modules.users.models import User
from app.shared.storage.interface import Storage


class FileService:
  def __init__(self, repo: FileRepository, storage: Storage):
    self.repo = repo
    self.storage = storage
  

  async def upload_picture(self, upload: UploadFile, user: User):
    extension = Path(upload.filename).suffix

    filename = f"{uuid4()}{extension}"

    path = await self.storage.upload(
      upload,
      filename,
      folder="pictures"
    )

    file = File(
      filename=filename,
      original_name=upload.filename,
      content_type=upload.content_type,
      path=path,
      size=upload.size,
      storage="local",
      uploaded_by=user.id
    )
    return await self.repo.create(file)
  
  
  async def get_file(self, file_id: UUID):
    file = await self.repo.get(file_id)

    if not file:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="File not found",
      )
    
    exists = await self.storage.exists(file.path)

    if not exists:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="File storage missing",
      )

    return file