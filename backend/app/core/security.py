import uuid
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend, BearerTransport, JWTStrategy)

from app.core.config import settings
from app.models.user import User
from app.db.adapters import get_user_db

# Configure Bearer token transport
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Configure JWT strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600) # 1 hour expiration

# Setup Authentication Backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Initialize FastAPIUsers
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_db,
    [auth_backend],
)

# Dependency for requiring an active, verified user
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
# Dependency for requiring an active superuser
current_active_superuser = fastapi_users.current_user(active=True, superuser=True) 