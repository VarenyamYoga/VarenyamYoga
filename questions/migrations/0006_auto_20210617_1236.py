# Generated by Django 3.0.5 on 2021-06-17 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_auto_20210615_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 17, 12, 36, 35, 44993)),
        ),
        migrations.AlterField(
            model_name='assessment_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 17, 12, 36, 35, 44993)),
        ),
    ]
