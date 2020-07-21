# Generated by Django 2.2 on 2020-07-19 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_auto_20200719_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='desc_tags',
            field=models.ManyToManyField(blank=True, to='core.DescriptiveTag'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.UserProfile'),
        ),
    ]
