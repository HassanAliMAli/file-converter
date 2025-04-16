import uuid
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.db.session import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    # Add any additional user fields here
    # Example: first_name: Mapped[str | None] = mapped_column(String(50))
    # Example: last_name: Mapped[str | None] = mapped_column(String(50))
    pass 