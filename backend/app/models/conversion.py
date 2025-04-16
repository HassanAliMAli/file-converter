import uuid
import datetime
from sqlalchemy import String, DateTime, ForeignKey, func, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db.session import Base

# Enum for conversion status
class ConversionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Conversion(Base):
    __tablename__ = "conversions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id: Mapped[str | None] = mapped_column(String, unique=True, index=True) # Celery task ID
    original_file_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id"))
    output_format: Mapped[str] = mapped_column(String)
    status: Mapped[ConversionStatus] = mapped_column(
        SqlEnum(ConversionStatus, name="conversion_status_enum", create_type=False),
        default=ConversionStatus.PENDING,
        index=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    converted_file_path: Mapped[str | None] = mapped_column(String) # Path to the converted file
    error_message: Mapped[str | None] = mapped_column(String)

    original_file: Mapped["File"] = relationship(back_populates="conversions") 