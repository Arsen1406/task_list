import time
from datetime import timedelta
from loguru import logger
from celery.worker.consumer import Tasks
from django.utils.timezone import now
from core.celery import app


@app.task
def delete_tasks():
    logger.info('Start deleting old tasks')
    date = now() - timedelta(days=14)
    queryset = Tasks.objects.filter(
        status='answer',
        update_date__gte=date
    )
    logger.info(f'{len(queryset)} objects are being deleted')
    for obj in queryset:
        obj.delete()


@app.task()
def change_status_task(instance, status):
    logger.info('Starting the task processing process')
    time.sleep(10)
    instance.status = status
    instance.update_date = now()
    instance.save()
    logger.info('Processing is completed. Status changed')
