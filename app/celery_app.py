from celery import Celery
from .config import settings

# Initialize Celery
celery_app = Celery(
    "worker",
    broker=settings.redis_url,          # redis://localhost:6379/0
    backend=settings.redis_url,          # Same Redis for results
    include=["app.tasks"]                 # Where tasks are defined
)

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=60,   # 60 seconds soft limit
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_default_retry_delay=300,  # 5 minutes
    task_max_retries=3,
)

# Beat schedule for periodic tasks (optional)
celery_app.conf.beat_schedule = {
    "cleanup-old-notifications": {
        "task": "app.tasks.cleanup_old_notifications",
        "schedule": 86400.0,  # Daily
    },
}