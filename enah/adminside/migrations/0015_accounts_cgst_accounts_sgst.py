# Generated by Django 4.2.1 on 2023-06-27 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0014_rename_product_sales_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='cgst',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='accounts',
            name='sgst',
            field=models.FloatField(default=0.0),
        ),
    ]
