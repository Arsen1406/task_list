# Generated by Django 3.2.19 on 2023-06-30 20:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20230630_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 30, 20, 50, 18, 526673, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='number',
            field=models.UUIDField(default=uuid.UUID('0576db84-f33e-49ca-9f3f-87474b50d981'), editable=False, unique=True, verbose_name='Номер задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='update_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 30, 20, 50, 18, 526673, tzinfo=utc), verbose_name='Дата обновления'),
        ),
    ]
