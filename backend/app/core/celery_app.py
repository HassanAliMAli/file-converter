from celery import Celery
from app.core.config import settings

# Initialize Celery
# The first argument is the name of the current module, important for autodiscovery
# The broker and backend URLs are taken from the main settings object
celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.worker.tasks'] # Specify where tasks are defined
)

# Optional Celery configuration (can also be in settings)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',          # Use UTC timezone
    enable_utc=True,
    # Add other Celery settings as needed
    # task_track_started=True,
    # worker_prefetch_multiplier=1,
)

if __name__ == '__main__':
    # Command to run worker: celery -A app.core.celery_app worker --loglevel=info
    # Ensure you run this from the 'backend' directory or adjust PYTHONPATH
    celery_app.start() 