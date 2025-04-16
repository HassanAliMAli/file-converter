from fastapi import FastAPI
from dotenv import load_dotenv
import os
import logging # Import logging
from fastapi.middleware.cors import CORSMiddleware # Import CORS

from app.core.security import fastapi_users, auth_backend
from app.schemas import UserRead, UserCreate
from app.routers import conversion # Import the conversion router

# Load environment variables from .env file
load_dotenv(dotenv_path='../.env') # Specify path relative to main.py

app = FastAPI(
    title="Universal File Converter API",
    description="API for the Universal File Converter web application.",
    version="0.1.0"
)

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure CORS
# TODO: Restrict origins in production
origins = [
    "http://localhost:5173", # Default Vite dev server port
    "http://localhost:3000", # Common React dev server port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)

@app.get("/health", tags=["health"])
async def health_check():
    # TODO: Add checks for DB, Redis connectivity if needed
    logger.info("Health check endpoint called.")
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