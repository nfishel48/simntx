# Generated by Django 2.2 on 2020-06-17 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_vendor_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='driver',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
