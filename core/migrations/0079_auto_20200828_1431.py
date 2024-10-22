# Generated by Django 2.2 on 2020-08-28 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_usernotificationsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotificationsettings',
            name='approved_denied',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usernotificationsettings',
            name='assigned_unassigned',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usernotificationsettings',
            name='cancelled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usernotificationsettings',
            name='created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usernotificationsettings',
            name='delivered',
            field=models.BooleanField(default=True),
        ),
    ]
