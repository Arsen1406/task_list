# Generated by Django 4.2.2 on 2023-06-30 16:09

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(verbose_name='Номер задачи')),
                ('status', models.CharField(choices=[('create', 'create'), ('processing', 'processing'), ('answer', 'answer')], max_length=20, verbose_name='Статус задачи')),
                ('create_date', models.DateField(default=django.utils.datetime_safe.datetime.now, verbose_name='Дата создания')),
                ('update_date', models.DateField(default=django.utils.datetime_safe.datetime.now, verbose_name='Дата обновления')),
            ],
        ),
    ]
