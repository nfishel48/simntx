# Generated by Django 2.2 on 2020-07-13 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20200713_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postimage',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ManyToManyField(blank=True, to='core.PostImage'),
        ),
    ]
