# Generated by Django 2.2 on 2020-07-03 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20200702_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
    ]
