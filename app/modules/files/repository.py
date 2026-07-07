from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.files.models import File

class FileRepository:
  def __init__(self, db: AsyncSession):
    self.db = db

  
  async def create(self, file: File):
    self.db.add(file)
    await self.db.commit()
    await self.db.refresh(file)
    return file


  async def get(self, file_id: UUID):
    return await self.db.get(File, file_id)