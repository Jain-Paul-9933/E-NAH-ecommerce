# Generated by Django 4.2.1 on 2023-06-22 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorside', '0017_rename_order_prepaidorder_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='payment_status',
            field=models.CharField(default='Not Paid', max_length=100),
        ),
    ]
