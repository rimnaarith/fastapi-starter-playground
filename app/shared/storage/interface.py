from abc import ABC, abstractmethod
from pathlib import Path
from fastapi import UploadFile


class Storage(ABC):

  @abstractmethod
  async def upload(
    self,
    file: UploadFile,
    filename: str,
    folder: str | None = None
  ) -> str:
    """
    Save file and return storage path.
    """

  @abstractmethod
  async def delete(self, path: str) -> None:
    """
    Delete stored file.
    """

  @abstractmethod
  async def exists(self, path: str) -> bool:
    """
    Check file exists.
    """

  @abstractmethod
  async def get_url(self, path: str) -> str:
    """
    Return accessible url.
    """

  @abstractmethod
  async def open(self, path: str) -> Path | bytes:
    """
    Return file for downloading.
    """