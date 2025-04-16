# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# Use asynchronous engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
# engine = create_engine(settings.DATABASE_URL, echo=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# Dependency to get DB session (asynchronous)
# def get_db():
async def get_db() -> AsyncSession:
    # db = SessionLocal()
    async with AsyncSessionLocal() as session:
        try:
            # yield db
            yield session
        finally:
            # db.close()
            await session.close() 