# Generated by Django 4.2.1 on 2023-06-06 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendordetails',
            name='license2',
            field=models.FileField(upload_to='vendor/license_2'),
        ),
    ]
