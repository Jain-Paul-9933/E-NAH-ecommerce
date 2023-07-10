# Generated by Django 4.2.1 on 2023-06-27 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0011_remove_accounts_days_remaining_for_rembursment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('bunch_order_id', models.CharField(max_length=100)),
                ('order_id', models.IntegerField()),
                ('vendor_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('product', models.CharField(max_length=100)),
                ('quantity_sold', models.IntegerField()),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]