"""
Celery Application for CIMEIKA
Handles asynchronous tasks
"""
import os
from celery import Celery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Celery
celery_app = Celery(
    'cimeika',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Auto-discover tasks from modules
# celery_app.autodiscover_tasks(['app', 'services'])


@celery_app.task
def example_task():
    """Example task for testing"""
    return "Task completed successfully"
