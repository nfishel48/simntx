# Generated by Django 2.2 on 2020-06-12 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='Blank'),
            preserve_default=False,
        ),
    ]
