# Generated by Django 2.2 on 2020-07-19 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_auto_20200719_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='vendor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_vendor', to='core.Vendor'),
        ),
    ]