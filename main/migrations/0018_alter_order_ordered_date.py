# Generated by Django 4.1.1 on 2022-12-01 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_order_id_alter_order_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 1, 10, 50, 0, 157102, tzinfo=datetime.timezone.utc)),
        ),
    ]
