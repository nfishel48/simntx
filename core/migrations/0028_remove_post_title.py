# Generated by Django 2.2 on 2020-06-24 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
