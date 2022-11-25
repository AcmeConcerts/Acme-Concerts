# Generated by Django 4.1.1 on 2022-11-25 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_orderticket_order_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderticket',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
