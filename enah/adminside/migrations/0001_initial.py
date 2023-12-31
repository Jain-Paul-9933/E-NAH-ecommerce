# Generated by Django 4.2.1 on 2023-06-01 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_1', models.CharField(max_length=100)),
                ('address_2', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='vendor/photo')),
                ('idProof', models.FileField(upload_to='vendor/id_proof')),
                ('license1', models.FileField(upload_to='vendor/license_1')),
                ('license2', models.FileField(upload_to='vendor/license2')),
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
