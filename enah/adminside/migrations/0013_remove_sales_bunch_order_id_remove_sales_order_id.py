# Generated by Django 4.2.1 on 2023-06-27 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0012_sales'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='bunch_order_id',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='order_id',
        ),
    ]
