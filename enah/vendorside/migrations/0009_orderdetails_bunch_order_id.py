# Generated by Django 4.2.1 on 2023-06-17 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorside', '0008_orderdetails_is_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='bunch_order_id',
            field=models.CharField(default=None, max_length=100, unique=True),
        ),
    ]
