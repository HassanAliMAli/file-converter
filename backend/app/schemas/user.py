import uuid
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    # Add custom fields exposed in read schema
    pass


class UserCreate(schemas.BaseUserCreate):
    # Add custom fields required during creation
    pass


class UserUpdate(schemas.BaseUserUpdate):
    # Add custom fields allowed during update
    pass 