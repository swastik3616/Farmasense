from app import create_app
from app.extensions import celery

app = create_app()
app.app_context().push()

# Import all tasks so that Celery worker discovers them
import app.tasks.communications
