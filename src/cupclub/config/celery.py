import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cupclub.config.settings")

app = Celery("cupclub")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
