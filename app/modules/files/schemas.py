from typing import Annotated

from fastapi import File, UploadFile
from pydantic import BaseModel

class FileUploadRequest(BaseModel):
  file: Annotated[UploadFile, File(description="Upload target file binary")]

class UploadResponse(BaseModel):
  id: str
  file_name: str