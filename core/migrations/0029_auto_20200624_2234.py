# Generated by Django 2.2 on 2020-06-25 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_remove_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='First', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='Last', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='links',
            field=models.ManyToManyField(blank=True, null=True, to='core.PostLink'),
        ),
    ]
