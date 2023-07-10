from tkinter import CASCADE
from django.db import models
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from userside.constants import PaymentStatus


class ProductDetails(models.Model):
    vendor_id = models.IntegerField(default=0,)
    productname = models.CharField(max_length=100)
    product_description = models.CharField(max_length=300)
    product_category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    img1 = models.ImageField(upload_to="product/images", null=True, blank=True)
    img2 = models.ImageField(upload_to="product/images", null=True, blank=True)
    img3 = models.ImageField(upload_to="product/images", null=True, blank=True)
    img4 = models.ImageField(upload_to="product/images", null=True, blank=True)
    is_active = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)
    is_listed = models.BooleanField(default=False)

    def __str__(self):
        return self.productname


class OrderDetails(models.Model):
    bunch_order_id = models.CharField(max_length=100)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100, default=None)
    product_image = models.ImageField(null=True, blank=True)
    user_id = models.IntegerField()
    address_id = models.IntegerField()
    vendor_id = models.IntegerField()
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    amount = models.IntegerField()
    coupon_id = models.IntegerField(default=0)
    bunch_order_amount = models.IntegerField(default=0)
    payment_type = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100, default="Not Paid")
    order_status = models.CharField(max_length=100)
    date_and_time = models.DateTimeField()
    is_canceled = models.BooleanField(default=False)
    is_closed_order = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class PrePaidOrder(models.Model):
    order_id = models.CharField(max_length=100)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"


class VendorNotification(models.Model):
    vendor_id = models.IntegerField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100, default=None)
    notification_content = models.CharField(max_length=300)
    date_and_time = models.DateTimeField()

    def __str__(self):
        return self.vendor_id, self.product_id, self.notification_content


class Coupon(models.Model):
    vendor_id = models.IntegerField()
    coupon_code = models.CharField(max_length=100)
    coupon_description = models.CharField(max_length=300)
    coupon_type = models.CharField(max_length=100)
    discount = models.FloatField()
    expiration_date = models.DateField()
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_description, self.coupon_type
