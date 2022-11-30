# Generated by Django 4.1.1 on 2022-11-27 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_orderticket_customized'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='location',
            field=models.CharField(default='No definido', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 27, 15, 28, 59, 536205, tzinfo=datetime.timezone.utc)),
        ),
    ]