# Generated by Django 4.2.1 on 2023-06-18 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0009_remove_accounts_days_remaining_for_rembursment'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='days_remaining_for_rembursment',
            field=models.IntegerField(default=0),
        ),
    ]
