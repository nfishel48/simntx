# Generated by Django 2.2 on 2020-07-08 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20200707_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=models.CharField(max_length=300),
        ),
    ]