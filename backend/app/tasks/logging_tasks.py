import logging
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.logging_tasks.log_activity")
def log_activity(user_id: str, activity: str):
    """
    Background task to log user activity.
    """
    logger.info(f"User {user_id} performed: {activity}")
    # Simulate some work or database write if needed
    return True
