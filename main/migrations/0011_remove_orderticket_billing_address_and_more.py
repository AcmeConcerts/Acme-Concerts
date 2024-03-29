# Generated by Django 4.1.1 on 2022-11-27 15:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_orderticket_billing_address_alter_order_ordered_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderticket',
            name='billing_address',
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.billingaddress'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 27, 15, 50, 33, 541357, tzinfo=datetime.timezone.utc)),
        ),
    ]
