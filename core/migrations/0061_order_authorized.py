# Generated by Django 2.2 on 2020-07-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_userprofile_is_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='authorized',
            field=models.BooleanField(default=False),
        ),
    ]