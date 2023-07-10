from calendar import MONDAY, TUESDAY
from email import message
from os import name
from django.shortcuts import render, redirect, HttpResponse
from adminside.models import VendorDetails, CustomUser, Accounts, Sales
from django.contrib.auth import authenticate, login, logout
from userside.models import CustomUser, Address
from vendorside.models import ProductDetails, OrderDetails, VendorNotification, Coupon
from django.template import loader
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render
import random
from django.contrib import messages


def adminhome(request):
    if request.user.is_authenticated and request.user.is_admin == True:
        products = ProductDetails.objects.filter(is_active=True)
        critical_stock = [product for product in products if product.quantity <= 20]
        today_date = datetime.now().date()
        k = OrderDetails.objects.filter(date_and_time__date=today_date).order_by(
            "-date_and_time"
        )
        daily_total_revenue = 0
        week_start_date = today_date - timedelta(days=today_date.weekday())
        week_end_date = week_start_date + timedelta(days=6)
        weekly_total_revenue = 0
        month_start_date = today_date.replace(day=1)
        month_end_date = month_start_date.replace(day=28) + timedelta(days=4)
        monthly_total_revenue = 0
        # Revenue showcasing area__________________________________________________________________________________________
        sales = (
            Sales.objects.all()
            .values("date")
            .annotate(total_revenue=Sum("revenue"))
            .order_by("date")
        )
        daily_revenue = (
            Sales.objects.filter(date=today_date)
            .values("product_name")
            .annotate(total_revenue=Sum("revenue"))
        )
        weekly_revenue = (
            Sales.objects.filter(date__range=[week_start_date, week_end_date])
            .values("product_name")
            .annotate(total_revenue=Sum("revenue"))
        )
        monthly_revenue = (
            Sales.objects.filter(date__range=[month_start_date, month_end_date])
            .values("product_name")
            .annotate(total_revenue=Sum("revenue"))
        )
        for sale in sales:
            if sale["date"] == today_date:
                daily_total_revenue += sale["total_revenue"]

        week_revenue_date = []
        week_revenue_data = []
        current_date = week_start_date
        while current_date <= week_end_date:
            week_revenue_date.append(str(current_date.strftime("%d-%m-%Y")))
            current_date_revenue = sales.filter(date=current_date).aggregate(
                total_revenue=Sum("total_revenue")
            )
            week_revenue_data.append(str(current_date_revenue["total_revenue"]))
            if current_date_revenue["total_revenue"]:
                weekly_total_revenue += current_date_revenue["total_revenue"]
            else:
                weekly_total_revenue += 0
            current_date += timedelta(days=1)

        month_revenue_date = []
        month_revenue_data = []
        current_date = month_start_date
        while current_date <= month_end_date:
            month_revenue_date.append(str(current_date.strftime("%d-%m-%Y")))
            current_date_revenue = sales.filter(date=current_date).aggregate(
                total_revenue=Sum("total_revenue")
            )
            month_revenue_data.append(str(current_date_revenue["total_revenue"]))
            if current_date_revenue["total_revenue"]:
                monthly_total_revenue += current_date_revenue["total_revenue"]
            else:
                monthly_total_revenue += 0
            current_date += timedelta(days=1)

        products = []
        product_color = []
        product_daily_revenue = []
        product_weekly_revenue = []
        product_monthly_revenue = []

        daily_revenue_product_list = []
        for revenue in daily_revenue:
            daily_revenue_product_list.append(revenue["product_name"])
        weekly_revenue_product_list = []
        for revenue in weekly_revenue:
            weekly_revenue_product_list.append(revenue["product_name"])

        monthly_revenue_product_list = []
        for revenue in monthly_revenue:
            monthly_revenue_product_list.append(revenue["product_name"])

        products_list = ProductDetails.objects.all()
        for product in products_list:
            products.append(product.productname)
            product_color.append(generate_hex_color())

            if product.productname in daily_revenue_product_list:
                for revenue in daily_revenue:
                    if revenue["product_name"] == product.productname:
                        product_daily_revenue.append(
                            str((revenue["total_revenue"] / daily_total_revenue) * 100)
                        )
            else:
                product_daily_revenue.append("0")

            if product.productname in weekly_revenue_product_list:
                for revenue in weekly_revenue:
                    if revenue["product_name"] == product.productname:
                        product_weekly_revenue.append(
                            str((revenue["total_revenue"] / weekly_total_revenue) * 100)
                        )
            else:
                product_weekly_revenue.append("0")

            if product.productname in monthly_revenue_product_list:
                for revenue in monthly_revenue:
                    if revenue["product_name"] == product.productname:
                        product_monthly_revenue.append(
                            str(
                                (revenue["total_revenue"] / monthly_total_revenue) * 100
                            )
                        )
            else:
                product_monthly_revenue.append("0")

        # revenue section ends here_______________________________________________________________________________
        # Order showcasing section________________________________________________________________________________
        today_orders = OrderDetails.objects.filter(date_and_time__date=today_date)
        week_orders = OrderDetails.objects.filter(
            date_and_time__date__range=(week_start_date, week_end_date)
        )
        month_orders = OrderDetails.objects.filter(
            date_and_time__date__range=(month_start_date, month_end_date)
        )
        today_orders_count = today_orders.count()
        week_orders_count = week_orders.count()
        month_orders_count = month_orders.count()

        week_order_date = []
        week_order_data = []
        current_date = week_start_date
        while current_date <= week_end_date:
            week_order_date.append(str(current_date.strftime("%d-%m-%Y")))
            week_order_data.append(
                OrderDetails.objects.filter(date_and_time__date=current_date).count()
            )
            current_date += timedelta(days=1)

        month_order_date = []
        month_order_data = []
        current_date = month_start_date
        while current_date <= month_end_date:
            month_order_date.append(str(current_date.strftime("%d-%m-%Y")))
            month_order_data.append(
                OrderDetails.objects.filter(date_and_time__date=current_date).count()
            )
            current_date += timedelta(days=1)

        # order section ends here________________________________________________________________________________
        context = {
            "s": k,
            "today_date": today_date,
            "daily_total_revenue": daily_total_revenue,
            "critical_stock": critical_stock,
            "week_revenue_date": week_revenue_date,
            "week_revenue_data": week_revenue_data,
            "week_start_date": week_start_date,
            "week_end_date": week_end_date,
            "weekly_total_revenue": weekly_total_revenue,
            "month_revenue_date": month_revenue_date,
            "month_revenue_data": month_revenue_data,
            "month_start_date": month_start_date,
            "month_end_date": month_end_date,
            "monthly_total_revenue": monthly_total_revenue,
            "daily_revenue": daily_revenue,
            "weekly_revenue": weekly_revenue,
            "monthly_revenue": monthly_revenue,
            "today_orders_count": today_orders_count,
            "week_orders_count": week_orders_count,
            "month_orders_count": month_orders_count,
            "week_order_date": week_order_date,
            "week_order_data": week_order_data,
            "month_order_date": month_order_date,
            "month_order_data": month_order_data,
            "products": products,
            "product_color": product_color,
            "product_daily_revenue": product_daily_revenue,
            "product_weekly_revenue": product_weekly_revenue,
            "product_monthly_revenue": product_monthly_revenue,
        }
        return render(request, "adminside/adminhome.html", context)
    else:
        return render(request, "adminside/adminlogin.html")


def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user and user.is_admin == True:
            login(request, user)
            return redirect("adminhome")
        else:
            return redirect("adminlogin")

    return render(request, "adminside/adminlogin.html")


def vendor_registration(request):
    if request.method == "POST":
        vendorname = request.POST.get("vendorName")
        email = request.POST.get("email")
        phone = request.POST.get("phoneNumber")
        password = request.POST.get("password")
        address1 = request.POST.get("addressLane1")
        address2 = request.POST.get("addressLane2")
        district = request.POST.get("district")
        pincode = request.POST.get("pincode")
        photo = request.FILES.get("photo")
        idproof = request.FILES.get("idProof")
        license1 = request.FILES.get("license1")
        license2 = request.FILES.get("license2")
        myvendor = CustomUser.objects.create_user(
            name=vendorname, email=email, phone=phone, password=password
        )
        myvendor.is_vendor = True
        myvendor.save()
        vendordata = VendorDetails(
            address_1=address1,
            address_2=address2,
            district=district,
            pincode=pincode,
            photo=photo,
            idProof=idproof,
            license1=license1,
            license2=license2,
            vendor=myvendor,
        )
        vendordata.save()
        return redirect("vendor_registration")

    if request.user.is_authenticated and request.user.is_admin == True:
        return render(request, "adminside/vendor_registration.html")
    else:
        return render(request, "adminside/adminlogin.html")


def userslist(request):
    if request.user.is_authenticated and request.user.is_admin == True:
        k = CustomUser.objects.filter(is_user=True).order_by("id")
        return render(request, "adminside/userslist.html", {"s": k})
    else:
        return render(request, "adminside/adminlogin.html")


def vendorslist(request):
    if request.user.is_authenticated and request.user.is_admin == True:
        k = CustomUser.objects.filter(is_vendor=True).order_by("id")
        return render(request, "adminside/vendorslist.html", {"s": k})
    else:
        return render(request, "adminside/adminlogin.html")


def adminproductslist(request):
    if request.user.is_authenticated and request.user.is_admin == True:
        k = ProductDetails.objects.all().order_by("id")
        return render(request, "adminside/adminproductslist.html", {"s": k})
    else:
        return render(request, "adminside/adminlogin.html")


def adminlogout(request):
    logout(request)
    return redirect("adminlogin")


def viewuser(request, id):
    if request.user.is_authenticated and request.user.is_admin == True:
        k = CustomUser.objects.get(id=id)
        return render(request, "adminside/viewuser.html", {"s": k})
    else:
        return render(request, "adminside/adminlogin.html")


def viewvendor(request, id):
    if request.user.is_authenticated and request.user.is_admin == True:
        k = VendorDetails.objects.get(vendor_id=id)
        j = CustomUser.objects.get(id=id)
        return render(request, "adminside/viewvendor.html", {"v": k, "u": j})
    else:
        return render(request, "adminside/adminlogin.html")


def blockuser(request, id):
    user = CustomUser.objects.get(id=id)
    product = ProductDetails.objects.filter(vendor_id=id).update(is_active=False)
    user.is_active = False
    user.save()
    if user.is_user is True:
        return redirect("userslist")
    else:
        return redirect("vendorslist")


def unblockuser(request, id):
    user = CustomUser.objects.get(id=id)
    product = ProductDetails.objects.filter(vendor_id=id).update(is_active=True)
    user.is_active = True
    user.save()
    if user.is_user is True:
        return redirect("userslist")
    else:
        return redirect("vendorslist")


def updatevendor(request, id):
    if request.user.is_authenticated and request.user.is_admin == True:
        k = VendorDetails.objects.get(vendor_id=id)
        j = CustomUser.objects.get(id=id)
        template = loader.get_template("adminside/vendor_updation.html")
        context = {"v": k, "u": j}
        return HttpResponse(template.render(context, request))
    else:
        return render(request, "adminside/adminlogin.html")


def vendor_updation(request, id):
    if request.method == "POST":
        vendorname = request.POST.get("vendorName")
        email = request.POST.get("email")
        phone = request.POST.get("phoneNumber")
        password = request.POST.get("password")
        address1 = request.POST.get("addressLane1")
        address2 = request.POST.get("addressLane2")
        district = request.POST.get("district")
        pincode = request.POST.get("pincode")
        photo = request.FILES.get("photo")
        idproof = request.FILES.get("idProof")
        license1 = request.FILES.get("license1")
        license2 = request.FILES.get("license2")
        myuser = CustomUser.objects.filter(id=id).update(
            name=vendorname, email=email, phone=phone, password=password
        )
        myvendor = VendorDetails.objects.filter(vendor_id=id).update(
            address_1=address1, address_2=address2, district=district, pincode=pincode
        )
        myvendorfile = VendorDetails.objects.get(vendor_id=id)
        myvendorfile.photo = photo
        myvendorfile.idProof = idproof
        myvendorfile.license1 = license1
        myvendorfile.license2 = license2
        myvendorfile.save()
        return redirect("vendorslist")


def admin_order_list(request):
    if request.user.is_authenticated and request.user.is_admin == True:
        k = OrderDetails.objects.all().order_by("-date_and_time")
        recieved_order_count = k.filter(order_status="Received").count()
        accepted_order_count = k.filter(order_status="Accepted").count()
        packed_order_count = k.filter(order_status="Packed").count()
        shipped_order_count = k.filter(order_status="Shipped").count()
        deliverd_order_count = k.filter(order_status="Deliverd").count()
        closed_order_count = k.filter(order_status="Order Closed").count()
        canceled_order_count = k.filter(order_status="Canceled").count()
        return render(
            request,
            "adminside/admin_order_list.html",
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
        return render(request, "adminside/adminlogin.html")


def admin_cancel_order(request, id):
    k = OrderDetails.objects.filter(id=id).update(
        order_status="Canceled", is_canceled=True
    )
    return redirect("admin_order_list")


def adminvieworder(request, id):
    if request.user.is_authenticated and request.user.is_admin == True:
        order = OrderDetails.objects.get(id=id)
        product_id = order.product_id  # standard assigning for understanding
        user_id = order.user_id
        vendor_id = order.vendor_id
        address_id = order.address_id
        product = ProductDetails.objects.get(id=product_id)
        user = CustomUser.objects.get(id=user_id)
        vendor = CustomUser.objects.get(id=vendor_id)
        address = Address.objects.get(id=address_id)
        return render(
            request,
            "adminside/vieworder.html",
            {
                "order": order,
                "product": product,
                "user": user,
                "address": address,
                "vendor": vendor,
            },
        )
    else:
        return render(request, "adminside/adminlogin.html")


def accounts(request):
    if request.user.is_authenticated and request.user.is_admin == True:
        accounts = Accounts.objects.all().order_by("-order_closed_date")
        total_amount_received = Accounts.objects.all().aggregate(
            total=Sum("amount_received")
        )
        total_platform_commision = Accounts.objects.all().aggregate(
            total=Sum("platform_commision")
        )
        total_vendor_rembursment = Accounts.objects.all().aggregate(
            total=Sum("vendor_rembursment")
        )
        return render(
            request,
            "adminside/accounts.html",
            {
                "accounts": accounts,
                "total_amount_received": total_amount_received["total"],
                "total_platform_commision": total_platform_commision["total"],
                "total_vendor_rembursment": total_vendor_rembursment["total"],
            },
        )


def admin_order_status_listing(request, status):
    if request.user.is_authenticated and request.user.is_admin == True:
        k = OrderDetails.objects.filter(order_status=status).order_by("-date_and_time")
        return render(
            request,
            "adminside/admin_order_status_listing.html",
            {"s": k, "status": status},
        )
    else:
        return render(request, "adminside/adminlogin.html")


def notify_vendor(request, vendor_id, id, productname):
    notification = VendorNotification(
        vendor_id=vendor_id,
        product_id=id,
        notification_content="Please,add " + productname + " stock,ASAP!!!",
        product_name=productname,
        date_and_time=datetime.now(),
    )
    notification.save()
    return redirect("adminhome")


def admin_coupon_list(request):
    coupons = Coupon.objects.all().order_by("is_disabled")
    return render(request, "adminside/admin_coupon_list.html", {"coupons": coupons})


def coupon_registration(request):
    if request.method == "POST":
        vendor_id = request.POST.get("vendor_id")
        coupon_code = request.POST.get("coupon_code")
        coupon_description = request.POST.get("coupon_description")
        coupon_type = request.POST.get("coupon_type")
        discount = request.POST.get("discount")
        expiration_date = request.POST.get("expiration_date")
        try:
            if VendorDetails.objects.get(vendor=vendor_id):
                pass
        except:
            messages.warning(request, "Enter a valid vendor id")
            return redirect("admin_coupon_list")

        new_coupon = Coupon.objects.create(
            vendor_id=vendor_id,
            coupon_code=coupon_code,
            coupon_description=coupon_description,
            coupon_type=coupon_type,
            discount=discount,
            expiration_date=expiration_date,
        )
        return redirect("admin_coupon_list")


def disable_enable_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    if coupon.is_disabled is True:
        new_status = False
    else:
        new_status = True
    coupon.is_disabled = new_status
    coupon.save()
    return redirect("admin_coupon_list")


def sales_report(request):
    # daily.....
    today = datetime.now().date()
    daily_sales = (
        Sales.objects.filter(date=today)
        .values("product_name")
        .annotate(
            total_quantity_sold=Sum("quantity_sold"), total_revenue=Sum("revenue")
        )
    )
    daily_total_revenue = 0
    for sale in daily_sales:
        daily_total_revenue += sale["total_revenue"]
    # weekly....
    week_start_date = today - timedelta(days=today.weekday())
    week_end_date = week_start_date + timedelta(days=6)
    weekly_sales = (
        Sales.objects.filter(date__range=[week_start_date, week_end_date])
        .values("product_name")
        .annotate(
            total_quantity_sold=Sum("quantity_sold"), total_revenue=Sum("revenue")
        )
    )
    weekly_total_revenue = 0
    for sale in weekly_sales:
        weekly_total_revenue += sale["total_revenue"]
    # monthly.....
    month_start_date = today.replace(day=1)
    month_end_date = month_start_date.replace(day=28) + timedelta(days=4)
    monthly_sales = (
        Sales.objects.filter(date__range=[month_start_date, month_end_date])
        .values("product_name")
        .annotate(
            total_quantity_sold=Sum("quantity_sold"), total_revenue=Sum("revenue")
        )
    )
    monthly_total_revenue = 0
    for sale in monthly_sales:
        monthly_total_revenue += sale["total_revenue"]

    return render(
        request,
        "adminside/sales_report.html",
        {
            "daily_sales": daily_sales,
            "today_date": today,
            "daily_total_revenue": daily_total_revenue,
            "weekly_sales": weekly_sales,
            "week_start_date": week_start_date,
            "week_end_date": week_end_date,
            "weekly_total_revenue": weekly_total_revenue,
            "monthly_sales": monthly_sales,
            "month_start_date": month_start_date,
            "month_end_date": month_end_date,
            "monthly_total_revenue": monthly_total_revenue,
        },
    )


def generate_hex_color():
    # Generate random RGB values
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Convert RGB to hex color code
    hex_code = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return hex_code
