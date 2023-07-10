# Generated by Django 4.2.1 on 2023-06-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0006_customuser_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('unit_price', models.IntegerField(default=0)),
                ('img1', models.ImageField(blank=True, null=True, upload_to='basket/itemimages')),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]