# Generated by Django 2.2 on 2020-06-29 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20200625_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='driver',
        ),
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver', to='core.UserProfile'),
        ),
    ]
