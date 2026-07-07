from app.core.config import settings

from app.shared.storage.local_storage import LocalStorage
from app.shared.storage.interface import Storage


def get_storage() -> Storage:

  if settings.STORAGE_DRIVER == "local":
    return LocalStorage(
      upload_dir=settings.UPLOAD_DIR
    )

  if settings.STORAGE_DRIVER == "s3":
    raise RuntimeError("S3 is not implemented.")

  raise RuntimeError("Unknown storage driver")