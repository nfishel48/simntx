# Generated by Django 2.2 on 2020-07-13 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_postlink_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='liked_posts',
            field=models.ManyToManyField(to='core.Post'),
        ),
    ]