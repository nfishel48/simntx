# Generated by Django 2.2 on 2020-06-15 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_item_vendor_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='vendor_id',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_id',
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]
