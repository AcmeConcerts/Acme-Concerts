# Generated by Django 4.1.1 on 2022-11-27 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_merge_20221127_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 27, 16, 18, 53, 690521, tzinfo=datetime.timezone.utc)),
        ),
    ]
