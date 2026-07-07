from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi.responses import FileResponse

from app.modules.auth.dependencies import get_current_user
from app.modules.files.dependencies import get_file_service
from app.modules.files.schemas import FileUploadRequest, UploadResponse
from app.modules.files.service import FileService
from app.modules.users.models import User


router = APIRouter()

@router.post("/uploads", response_model=UploadResponse)
async def upload(
  file: Annotated[FileUploadRequest, Form(media_type="multipart/form-data")],
  current_user: User = Depends(get_current_user),
  service: FileService = Depends(get_file_service)
):
  uploaded_file = await service.upload_picture(upload=file.file, user=current_user)
  return UploadResponse(
    id=str(uploaded_file.id),
    file_name=uploaded_file.original_name
  )

# Serve file through FastAPI
@router.get("/uploads/{file_id}")
async def get_file(file_id: UUID, service: FileService = Depends(get_file_service)):
  file = await service.get_file(file_id)
  return FileResponse(
    path=file.path,
    media_type=file.content_type,
    filename=file.original_name,
    content_disposition_type="inline"
  )
  