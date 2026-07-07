from uuid import UUID, uuid4

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class File(Base):
  __tablename__ = "files"

  id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
  filename: Mapped[str] = mapped_column(String, nullable=False)
  original_name: Mapped[str] = mapped_column(String, nullable=False)
  content_type: Mapped[str] = mapped_column(String, nullable=False)
  size: Mapped[int] = mapped_column(BigInteger, nullable=False)

  path: Mapped[str] = mapped_column(String, nullable=False)
  storage: Mapped[str] = mapped_column(String(10), nullable=False)

  uploaded_by: Mapped[str] = mapped_column(
    Uuid,
    ForeignKey("users.id"),
    nullable=False,
  )

  created_at = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False,
  )