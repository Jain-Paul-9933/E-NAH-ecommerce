# Generated by Django 4.2.1 on 2023-06-11 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0015_alter_basket_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('full_name', models.CharField(max_length=100)),
                ('address_lane_1', models.CharField(max_length=300)),
                ('address_lane_2', models.CharField(max_length=300)),
                ('city_or_town', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('pincode', models.IntegerField()),
                ('phone_number', models.IntegerField()),
                ('alt_phone_number', models.IntegerField()),
                ('land_mark', models.CharField(max_length=200)),
            ],
        ),
    ]
