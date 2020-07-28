# Generated by Django 2.2 on 2020-07-19 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_auto_20200719_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='vendor_id',
        ),
        migrations.AddField(
            model_name='order',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_vendor', to='core.Vendor'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address', to='core.Address'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='hours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hours', to='core.VendorHours'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.UserProfile'),
        ),
    ]