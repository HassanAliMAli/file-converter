from fastapi import FastAPI
# Remove dotenv import if load_dotenv is not used
# from dotenv import load_dotenv
import os
import logging # Import logging
from fastapi.middleware.cors import CORSMiddleware # Import CORS
from contextlib import asynccontextmanager # For lifespan events
from fastapi import status

# --- Rate Limiting Imports ---
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
# --- End Rate Limiting Imports ---

from app.core.security import fastapi_users, auth_backend
# from app.schemas import UserRead, UserCreate, UserUpdate # Import UserRead, UserCreate, UserUpdate
from app.schemas.user import UserRead, UserCreate, UserUpdate # Import UserRead, UserCreate, UserUpdate
from app.routers import conversion # Import the conversion router
from app.core.config import settings # Import settings
from app.db.session import init_engine, dispose_engine # Import engine lifecycle functions

# --- Rate Limiting Setup ---
limiter = Limiter(key_func=get_remote_address, default_limits=["1000/hour", "100/minute"])
# --- End Rate Limiting Setup ---

# Load environment variables from .env file
# load_dotenv(dotenv_path='../.env') # Specify path relative to main.py
# Recommend using Pydantic settings in app.core.config instead

# --- App Lifecycle Setup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing database engine...")
    init_engine() # Initialize the database engine
    logger.info("Database engine initialized.")
    yield
    # Shutdown
    logger.info("Disposing database engine...")
    await dispose_engine() # Dispose the database engine
    logger.info("Database engine disposed.")
# --- End App Lifecycle Setup ---

app = FastAPI(
    title="Universal File Converter API",
    description="API for the Universal File Converter web application.",
    version="0.1.0",
    lifespan=lifespan # Use new lifespan context manager
)

# --- Add Rate Limiter State and Handler ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# --- End Rate Limiter State and Handler ---

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure CORS
# Use origins defined in app.core.config.settings
# TODO: Restrict allow_methods and allow_headers further in production if needed

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS, # Use configured origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], # More specific methods
    allow_headers=["Content-Type", "Authorization"], # Common required headers
)

@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health_check():
    # TODO: Add checks for DB, Redis connectivity if needed
    # For now, just confirms the API is running
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Welcome to the Universal File Converter API"}

# Include FastAPI Users authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Include FastAPI Users registration routes
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Include FastAPI Users reset password routes
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# Include FastAPI Users verify routes
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

# Include FastAPI Users user management routes
app.include_router(
    # TODO: Ensure UserUpdate schema in app/schemas/user.py includes all intended updatable fields.
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Placeholder for future application-specific routers
app.include_router(conversion.router, prefix="/convert", tags=["conversion"]) # Include conversion router
# from .routers import admin # Assuming routers are in backend/app/routers
# app.include_router(admin.router)

if __name__ == "__main__":
    import uvicorn
    # Use environment variables for host and port if available, otherwise default
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    # Run from the project root directory usually, so app is referenced correctly
    # uvicorn.run("backend.main:app", host=host, port=port, reload=True)
    # If running main.py directly:
    uvicorn.run("main:app", host=host, port=port, reload=True) 