from logging import critical
from time import timezone
from django.shortcuts import render, redirect, HttpResponse
from userside.views import productsdisplay
from vendorside.models import ProductDetails, OrderDetails, VendorNotification, Coupon
from userside.models import Address, Basket
from userside.models import CustomUser
from adminside.models import Accounts, VendorDetails, Sales
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.utils import timezone
from datetime import datetime, timedelta


def vendorhome(request):
    if request.user.is_authenticated and request.user.is_vendor == True:
        notifications = VendorNotification.objects.filter(vendor_id=request.user.id)
        products = ProductDetails.objects.filter(
            vendor_id=request.user.id, is_active=True
        )
        critical_stock = [product for product in products if product.quantity <= 20]
        today_date = datetime.now().date()
        k = OrderDetails.objects.filter(
            vendor_id=request.user.id, date_and_time__date=today_date
        ).order_by("-date_and_time")
        return render(
            request,
            "vendorside/vendorhome.html",
            {
                "s": k,
                "today_date": today_date,
                "critical_stock": critical_stock,
                "notifications": notifications,
            },
        )
    else:
        return render(request, "vendorside/vendorlogin.html")


def vendorlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user and user.is_vendor == True and user.is_active == True:
            login(request, user)
            return redirect("vendorhome")
        else:
            return redirect("vendorlogin")

    return render(request, "vendorside/vendorlogin.html")


def product_registration(request):
    if request.method == "POST":
        productname = request.POST.get("product_name")
        product_description = request.POST.get("product_description")
        product_category = request.POST.get("product_category")
        quantity = request.POST.get("quantity")
        unit_price = request.POST.get("unit_price")
        img1 = request.FILES.get("image1")
        img2 = request.FILES.get("image2")
        img3 = request.FILES.get("image3")
        img4 = request.FILES.get("image4")
        productdata = ProductDetails(
            productname=productname,
            product_description=product_description,
            product_category=product_category,
            quantity=quantity,
            unit_price=unit_price,
            img1=img1,
            img2=img2,
            img3=img3,
            img4=img4,
            is_active=True,
            vendor_id=request.user.id,
        )
        productdata.save()
        return redirect("productslist")

    if request.user.is_authenticated and request.user.is_vendor == True:
        return render(request, "vendorside/product_registration.html")
    else:
        return render(request, "vendorside/vendorlogin.html")


def productslist(request):
    if request.user.is_authenticated and request.user.is_vendor == True:
        k = ProductDetails.objects.filter(vendor_id=request.user.id).order_by("id")
        return render(request, "vendorside/productslist.html", {"s": k})
    else:
        return render(request, "vendorside/vendorlogin.html")


def vendorlogout(request):
    logout(request)
    return redirect("vendorlogin")


def vendorviewproduct(request, id):
    if request.user.is_authenticated and request.user.is_vendor == True:
        k = ProductDetails.objects.get(vendor_id=request.user.id, id=id)
        return render(request, "vendorside/vendorviewproduct.html", {"s": k})
    else:
        return render(request, "vendorside/vendorlogin.html")


def blockproduct(request, id):
    product = ProductDetails.objects.filter(id=id).update(is_active=False)
    return redirect("productslist")


def unblockproduct(request, id):
    product = ProductDetails.objects.filter(id=id).update(is_active=True)
    return redirect("productslist")


def updateproduct(request, id):
    if request.user.is_authenticated and request.user.is_vendor == True:
        k = ProductDetails.objects.get(id=id)
        template = loader.get_template("vendorside/product_updation.html")
        context = {"p": k}
        return HttpResponse(template.render(context, request))
    else:
        return render(request, "vendorside/vendorlogin.html")


def product_updation(request, id):
    if request.method == "POST":
        productname = request.POST.get("product_name")
        product_description = request.POST.get("product_description")
        product_category = request.POST.get("product_category")
        unit_price = request.POST.get("unit_price")
        img1 = request.FILES.get("image1")
        img2 = request.FILES.get("image2")
        img3 = request.FILES.get("image3")
        img4 = request.FILES.get("image4")
        productdata = ProductDetails.objects.filter(id=id).update(
            productname=productname,
            product_description=product_description,
            product_category=product_category,
            unit_price=unit_price,
        )
        productfile = ProductDetails.objects.get(id=id)
        productfile.img1 = img1
        productfile.img2 = img2
        productfile.img3 = img3
        productfile.img4 = img4
        productfile.save()
        return redirect("productslist")


def order_list(request):
    if request.user.is_authenticated and request.user.is_vendor == True:
        k = OrderDetails.objects.filter(vendor_id=request.user.id).order_by(
            "-date_and_time"
        )
        recieved_order_count = k.filter(order_status="Received").count()
        accepted_order_count = k.filter(order_status="Accepted").count()
        packed_order_count = k.filter(order_status="Packed").count()
        shipped_order_count = k.filter(order_status="Shipped").count()
        deliverd_order_count = k.filter(order_status="Deliverd").count()
        closed_order_count = k.filter(order_status="Order Closed").count()
        canceled_order_count = k.filter(order_status="Canceled").count()
        return render(
            request,
            "vendorside/order_list.html",
            {
                "s": k,
                "recieved_order_count": recieved_order_count,
                "accepted_order_count": accepted_order_count,
                "packed_order_count": packed_order_count,
                "shipped_order_count": shipped_order_count,
                "deliverd_order_count": deliverd_order_count,
                "closed_order_count": closed_order_count,
                "canceled_order_count": canceled_order_count,
            },
        )
    else:
        return render(request, "vendorside/vendorlogin.html")


# The below functions can be also written as single function
# for accepting,canceling,packing and shipping an change the
#  function anme to status changer


def accept_order(request, id):
    k = OrderDetails.objects.filter(id=id, vendor_id=request.user.id).update(
        order_status="Accepted"
    )
    return redirect("order_list")


def pack_order(request, id):
    k = OrderDetails.objects.filter(id=id, vendor_id=request.user.id).update(
        order_status="Packed"
    )
    return redirect("order_list")


def ship_order(request, id):
    k = OrderDetails.objects.filter(id=id, vendor_id=request.user.id).update(
        order_status="Shipped"
    )
    return redirect("order_list")


def deliverd_order(request, id):
    k = OrderDetails.objects.filter(id=id, vendor_id=request.user.id).update(
        order_status="Deliverd", payment_status="Paid"
    )
    return redirect("order_list")


def cancel_order(request, id):
    canceled_order = OrderDetails.objects.get(id=id)
    product = ProductDetails.objects.get(id=canceled_order.product_id)
    product.quantity += canceled_order.quantity
    product.save()
    k = OrderDetails.objects.filter(id=id, vendor_id=request.user.id).update(
        order_status="Canceled", is_canceled=True
    )
    print(product)
    return redirect("order_list")


def close_order(request, id):
    k = OrderDetails.objects.get(id=id)
    platform_commision = (k.amount * 5) / 100
    cgst = (k.amount * 5) / 100
    sgst = (k.amount * 5) / 100
    vendor_rembursment = k.amount - platform_commision - cgst - sgst
    entry_to_accounts = Accounts(
        order_id=k.id,
        vendor_id=k.vendor_id,
        amount_received=k.amount,
        platform_commision=platform_commision,
        vendor_rembursment=vendor_rembursment,
        order_closed_date=datetime.now().date(),
        order_rembursment_due_date=(datetime.now() + timedelta(days=15)).date(),
        cgst=cgst,
        sgst=sgst,
    )
    """item_exists=Sales.objects.filter(date=datetime.now().date(),vendor_id=k.vendor_id,product_id=k.product_id)
    if item_exists:
        item_exists.quantity_sold+=k.quantity
        item_exists.revenue+=k.amount
        item_exists.save()
    else:"""
    entry_to_sales = Sales(
        date=datetime.now().date(),
        vendor_id=k.vendor_id,
        product_id=k.product_id,
        product_name=k.product_name,
        quantity_sold=k.quantity,
        revenue=k.amount,
    )
    entry_to_sales.save()
    entry_to_accounts.save()
    m = OrderDetails.objects.filter(id=id, vendor_id=request.user.id).update(
        order_status="Order Closed", is_closed_order=True
    )

    return redirect("order_list")


def vendorvieworder(request, id):
    if request.user.is_authenticated and request.user.is_vendor == True:
        order = OrderDetails.objects.get(id=id)
        product_id = order.product_id  # standard assigning for understanding
        user_id = order.user_id
        address_id = order.address_id
        product = ProductDetails.objects.get(id=product_id)
        user = CustomUser.objects.get(id=user_id)
        address = Address.objects.get(id=address_id)
        vendor = CustomUser.objects.get(id=order.vendor_id)
        return render(
            request,
            "vendorside/vieworder.html",
            {
                "order": order,
                "product": product,
                "user": user,
                "address": address,
                "vendor": vendor,
            },
        )
    else:
        return render(request, "vendorside/vendorlogin.html")


def order_status_listing(request, status):
    if request.user.is_authenticated and request.user.is_vendor == True:
        k = OrderDetails.objects.filter(
            vendor_id=request.user.id, order_status=status
        ).order_by("-date_and_time")
        return render(
            request, "vendorside/order_status_listing.html", {"s": k, "status": status}
        )
    else:
        return render(request, "vendorside/vendorlogin.html")


def update_status_all(request, status):
    if status == "Received":
        new_status = "Accepted"
    elif status == "Accepted":
        new_status = "Packed"
    elif status == "Packed":
        new_status = "Shipped"
    elif status == "Shipped":
        new_status = "Deliverd"
    elif status == "Deliverd":
        new_status = "Order Closed"
    if new_status == "Deliverd":
        update = OrderDetails.objects.filter(
            vendor_id=request.user.id, order_status=status
        ).update(order_status=new_status, payment_status="Paid")
    else:
        update = OrderDetails.objects.filter(
            vendor_id=request.user.id, order_status=status
        ).update(order_status=new_status)
    return redirect(order_status_listing, status=status)


def stock(request):
    if request.user.is_authenticated and request.user.is_vendor == True:
        products = ProductDetails.objects.filter(
            vendor_id=request.user.id, is_active=True
        ).order_by("productname")
        return render(request, "vendorside/stock.html", {"products": products})
    else:
        return render(request, "vendorside/vendorlogin.html")


def update_stock(request, id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))
        update_type = request.POST.get("update_type")
        product = ProductDetails.objects.get(id=id)
        if update_type == "+":
            if quantity <= 500 - product.quantity:
                new_quantity = product.quantity + quantity
            else:
                new_quantity = 500
        else:
            if quantity <= product.quantity:
                new_quantity = product.quantity - quantity
            else:
                new_quantity = 0
        product.quantity = new_quantity
        product.save()
        return redirect("stock")


def delete_notification(request, id):
    notification = VendorNotification.objects.filter(id=id).delete()
    return redirect("vendorhome")


def coupon_list(request):
    coupons = Coupon.objects.filter(vendor_id=request.user.id).order_by("is_disabled")
    return render(request, "vendorside/coupon_list.html", {"coupons": coupons})
