# Generated by Django 4.2.1 on 2023-06-25 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0018_address_is_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=200)),
                ('img1', models.ImageField(blank=True, null=True, upload_to='wishlist/itemimages')),
                ('listed', models.BooleanField(default=False)),
            ],
        ),
    ]