# Generated by Django 2.2 on 2020-06-18 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_item_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='category',
        ),
    ]