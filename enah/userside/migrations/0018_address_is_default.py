# Generated by Django 4.2.1 on 2023-06-23 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0017_alter_address_alt_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
