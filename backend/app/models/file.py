import uuid
import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base
from app.models.user import User # Import User for relationship

class File(Base):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_filename: Mapped[str] = mapped_column(String, index=True)
    storage_path: Mapped[str] = mapped_column(String, unique=True) # Path in temp storage or cloud
    content_type: Mapped[str | None] = mapped_column(String)
    file_size: Mapped[int | None] = mapped_column(Integer) # Size in bytes
    uploaded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))

    owner: Mapped["User"] = relationship(back_populates="files", lazy="selectin")
    conversions: Mapped[list["Conversion"]] = relationship(back_populates="original_file")

# Add back-population to User model
User.files = relationship("File", order_by=File.id, back_populates="owner") 