# Generated by Django 2.2 on 2020-08-22 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_order_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='token',
        ),
    ]