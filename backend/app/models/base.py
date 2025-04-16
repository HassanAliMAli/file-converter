from app.db.session import Base

# Import all the models, so that Base has them before being
# imported by Alembic
# This assumes you will have models defined in other files in this directory
# e.g., from .user import User
# e.g., from .file import File 