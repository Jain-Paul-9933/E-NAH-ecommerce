# Generated by Django 4.2.1 on 2023-07-01 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorside', '0029_rename_coupon_orderdetails_coupon_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='unit_price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]