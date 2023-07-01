import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

User = get_user_model()


class Task(models.Model):

    CREATE = 'create'
    PROCESSING = 'processing'
    ANSWER = 'answer'

    id = models.AutoField(primary_key=True)
    number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name='Номер задачи'
    )
    status = models.CharField(
        default=CREATE,
        max_length=20,
        verbose_name='Статус задачи'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='task',
        verbose_name='Исполнитель'
    )
    create_date = models.DateTimeField(
        default=now,
        verbose_name='Дата создания'
    )
    update_date = models.DateTimeField(
        default=now,
        verbose_name='Дата обновления'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
