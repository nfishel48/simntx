# Generated by Django 2.2 on 2020-06-12 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200612_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test_product'),
            preserve_default=False,
        ),
    ]
