from app import create_app
from app.extensions import celery

app = create_app()
app.app_context().push()

# Import all tasks so that Celery worker discovers them
import app.tasks.communications
from app.tasks.weather_monitor import monitor_farm_weather

from celery.schedules import crontab

# Celery Beat schedule for autonomous proactive triggers
celery.conf.beat_schedule = {
    'monitor_weather_every_12_hours': {
        'task': 'tasks.monitor_farm_weather',
        'schedule': crontab(minute=0, hour='*/12'), # Twice daily execution
    },
}
celery.conf.timezone = 'UTC'
