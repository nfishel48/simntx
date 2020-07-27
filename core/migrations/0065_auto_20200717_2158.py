# Generated by Django 2.2 on 2020-07-18 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_auto_20200717_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='tags',
            new_name='general_tags',
        ),
        migrations.AddField(
            model_name='item',
            name='desc_tags',
            field=models.ManyToManyField(to='core.DescriptiveTag'),
        ),
    ]
