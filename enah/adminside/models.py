from django.db import models
from userside.models import CustomUser


class VendorDetails(models.Model):
    vendor = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    district = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="vendor/photo", null=True, blank=True)
    idProof = models.FileField(upload_to="vendor/id_proof")
    license1 = models.FileField(upload_to="vendor/license_1")
    license2 = models.FileField(upload_to="vendor/license_2")

    def __str__(self):
        return self.vendor.name


class Accounts(models.Model):
    order_id = models.IntegerField()
    vendor_id = models.IntegerField()
    amount_received = models.FloatField()
    platform_commision = models.FloatField()
    cgst = models.FloatField(default=0.0)
    sgst = models.FloatField(default=0.0)
    vendor_rembursment = models.FloatField()
    order_closed_date = models.DateTimeField(default=None)
    order_rembursment_due_date = models.DateTimeField(default=None)

    def __str__(self):
        return self.order_id


class Sales(models.Model):
    date = models.DateField()
    vendor_id = models.IntegerField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    quantity_sold = models.IntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
