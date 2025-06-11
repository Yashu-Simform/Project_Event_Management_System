import os

from celery import Celery
from celery.schedules import crontab
from time import sleep
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("Event_Management_System")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task
def add(x, y):
    sleep(20)
    return x + y


# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')


# app.conf.beat_schedule = {
#     "event_reminder": {
#         "task": "api.tasks.send_reminder_mail",
#         "schedule": crontab(minute=10),
#     }
# }

app.conf.beat_schedule = {
    'tomorrow_events': {
        'task': 'api.tasks.tomorrow_events_mail',
        'schedule': crontab(hour=settings.TOMORROW_EVENT_EMAIL_HOUR,minute=settings.TOMORROW_EVENT_EMAIL_MINUTE),
    },
}
app.conf.timezone = 'Asia/Kolkata'