# Generated by Django 4.2.1 on 2023-06-22 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendorside', '0014_rename_order_prepaidorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prepaidorder',
            name='name',
        ),
    ]