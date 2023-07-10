from itertools import product
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from vendorside.models import Coupon
from userside.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]

    objects = CustomUserManager()

    def __str__(self):
        return "{}".format(self.email)


class Basket(models.Model):
    user_id = models.IntegerField(default=0)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    img1 = models.ImageField(upload_to="basket/itemimages", null=True, blank=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class Address(models.Model):
    user_id = models.IntegerField()
    full_name = models.CharField(max_length=100)
    address_lane_1 = models.CharField(max_length=300)
    address_lane_2 = models.CharField(max_length=300)
    city_or_town = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone_number = models.CharField(max_length=100)
    alt_phone_number = models.CharField(max_length=100)
    land_mark = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Wishlist(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    img1 = models.ImageField(upload_to="wishlist/itemimages", null=True, blank=True)
    listed = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class UserCouponsApplied(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    is_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name, self.coupon.coupon_code
