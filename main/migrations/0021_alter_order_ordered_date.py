# Generated by Django 4.1.1 on 2022-12-01 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_order_ordered_date_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 1, 12, 50, 53, 200068, tzinfo=datetime.timezone.utc)),
        ),
    ]
