# Generated by Django 2.2 on 2020-06-24 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200623_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='Post title', max_length=100),
            preserve_default=False,
        ),
    ]
