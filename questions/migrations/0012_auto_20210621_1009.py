# Generated by Django 3.0.5 on 2021-06-21 04:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_auto_20210618_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 21, 10, 9, 20, 725863)),
        ),
        migrations.AlterField(
            model_name='assessment_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 21, 10, 9, 20, 725863)),
        ),
    ]