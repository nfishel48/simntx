# Generated by Django 2.2 on 2020-06-18 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20200617_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='owner',
        ),
    ]
