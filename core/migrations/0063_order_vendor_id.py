# Generated by Django 2.2 on 2020-07-16 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_merge_20200715_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='vendor_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_id', to='core.Vendor'),
        ),
    ]
