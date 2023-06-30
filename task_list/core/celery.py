import os
from celery import Celery
from task_list import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_list.settings')

app = Celery('MANAGER_TASKS')

app.config_from_object("django.conf:settings")
app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks()
