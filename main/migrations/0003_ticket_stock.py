# Generated by Django 4.1.1 on 2022-11-24 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_ticket_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='stock',
            field=models.PositiveIntegerField(default=10),
        ),
    ]