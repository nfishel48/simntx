# Generated by Django 2.2 on 2020-07-13 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_auto_20200713_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlink',
            name='title',
            field=models.CharField(default='Link Title', max_length=50),
        ),
    ]
