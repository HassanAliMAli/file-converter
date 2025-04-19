# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# This line causes issues when imported by Alembic before the app fully loads settings
# engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# We will create the engine later, likely during FastAPI app startup
engine = None # Placeholder

# Ensure Base is defined before SessionLocal
Base = declarative_base()

# Configure SessionLocal after Base is defined
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine, # SessionLocal will bind to the engine once it's created
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get DB session
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# Function to initialize the database engine (call this during app startup)
def init_engine():
    global engine
    if engine is None:
        engine = create_async_engine(settings.DATABASE_URL, echo=settings.DB_ECHO_LOG, future=True, pool_pre_ping=True)
        # Re-bind SessionLocal to the created engine
        SessionLocal.configure(bind=engine)

# Function to dispose the engine (call this during app shutdown)
async def dispose_engine():
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None 