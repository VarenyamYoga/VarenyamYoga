# Generated by Django 3.0.5 on 2021-06-15 08:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20210615_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 15, 13, 45, 23, 914544)),
        ),
        migrations.AlterField(
            model_name='assessment_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 15, 13, 45, 23, 914544)),
        ),
    ]