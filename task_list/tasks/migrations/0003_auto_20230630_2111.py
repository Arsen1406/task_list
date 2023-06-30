# Generated by Django 3.2.19 on 2023-06-30 18:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['id'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AlterField(
            model_name='task',
            name='number',
            field=models.CharField(default=uuid.UUID('df5efbfd-8750-4430-875d-c9c213a9ecb5'), max_length=244, unique=True, verbose_name='Номер задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='create', max_length=20, verbose_name='Статус задачи'),
        ),
    ]
