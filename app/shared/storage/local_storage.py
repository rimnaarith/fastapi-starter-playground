import aiofiles
from pathlib import Path

from fastapi import UploadFile

from app.shared.storage.interface import Storage


class LocalStorage(Storage):

  def __init__(self, upload_dir: str = "uploads"):
    self.upload_dir = Path(upload_dir)
    self.upload_dir.mkdir(exist_ok=True)


  async def upload(
    self,
    file: UploadFile,
    filename: str,
    folder: str | None = None
  ) -> str:

    directory = self.upload_dir

    if folder:
      directory = directory / folder
      directory.mkdir(parents=True, exist_ok=True)

    filepath = directory / filename

    async with aiofiles.open(filepath, "wb") as f:

      while chunk := await file.read(1024 * 1024):
        await f.write(chunk)

    return str(filepath)


  async def delete(self, path: str):

    Path(path).unlink(missing_ok=True)


  async def exists(self, path: str):

    return Path(path).exists()


  async def get_url(self, path: str):

    return f"/api/files/download?path={path}"


  async def open(self, path: str):

    return Path(path)