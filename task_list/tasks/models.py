from django.contrib.auth import get_user_model
from django.db import models
from django.utils.datetime_safe import datetime

User = get_user_model()


class Task(models.Model):
    number = models.IntegerField(
        verbose_name='Номер задачи'
    )
    status = models.CharField(
        max_length=200,
        verbose_name='Статус задачи'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='task',
        verbose_name='Исполнитель'
    )
    create_date = models.DateField(
        default=datetime.now,
        verbose_name='Дата создания'
    )
    update_date = models.DateField(
        default=datetime.now,
        verbose_name='Дата обновления'
    )
