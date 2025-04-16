import uuid
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User


async def get_user_db(session: AsyncSession = Depends(get_db)) -> SQLAlchemyUserDatabase[User, uuid.UUID]:
    yield SQLAlchemyUserDatabase(session, User) 