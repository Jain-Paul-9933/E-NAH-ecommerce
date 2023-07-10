from statistics import quantiles
from unicodedata import category
from django.shortcuts import render, redirect, HttpResponse
from vendorside.models import ProductDetails, OrderDetails, PrePaidOrder, Coupon
from adminside.models import VendorDetails
from userside.models import CustomUser, Basket, Address, Wishlist, UserCouponsApplied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from . import verify
from django.template import loader
from django.db.models import Sum
from django.contrib import messages
import re
from django.utils import timezone
import uuid

# import time
# import random
from django.views.decorators.csrf import csrf_exempt
import razorpay
from enah.settings import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
)
from .constants import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
import json
from django.template.loader import render_to_string


def index(request):
    if request.user.is_anonymous:
        return render(request, "userside/index.html")
    elif request.user.is_vendor == True or request.user.is_admin == True:
        logout(request)
        return render(request, "userside/index.html")
    return render(request, "userside/index.html", {"count": basket_count(request)})


def usersignup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = "+91" + request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation from here
        nameRegex = r"^[a-zA-Z\s]+$"
        emailRegex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        phoneRegex = r"^(\+91|0)?[6789]\d{9}$"
        passwordRegex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        if not re.match(nameRegex, name):
            messages.warning(request, "Name is not valid")
            return redirect("usersignup")
        elif not re.match(emailRegex, email):
            messages.warning(request, "Email is not valid")
            return redirect("usersignup")
        elif not re.match(phoneRegex, phone):
            messages.warning(
                request,
                "Phone number is not valid,Please Enter the 10-digit Mobile Number",
            )
            return redirect("usersignup")
        elif not re.match(passwordRegex, password):
            messages.warning(
                request,
                "Password is not valid. It should contain at least 8 characters, one uppercase letter, one lowercase letter, and one digit.",
            )
            return redirect("usersignup")
        elif not re.match(passwordRegex, confirm_password):
            messages.warning(
                request,
                "Confirm Password is not valid. It should contain at least 8 characters, one uppercase letter, one lowercase letter, and one digit.",
            )
            return redirect("usersignup")
        elif password != confirm_password:
            messages.warning(request, "Password is not macthing with Confirm Password")
            return redirect("usersignup")
        elif CustomUser.objects.filter(email=email):
            messages.warning(request, "Email is already taken")
            return redirect("usersignup")
        elif CustomUser.objects.filter(phone=phone):
            messages.warning(request, "Phone number is already taken")
            return redirect("usersignup")
        else:
            # Validation ends here
            try:
                verify.send(phone)
            except:
                return HttpResponse("Check your Internet Connection")
            myuser = CustomUser.objects.create_user(
                name=name, email=email, phone=phone, password=password
            )
            myuser.is_user = True
            myuser.save()
            return render(
                request,
                "userside/otpverification.html",
                {"id": myuser.id, "phone": myuser.phone},
            )

    if request.user.is_authenticated:
        return render(request, "userside/index.html")
    else:
        return render(request, "userside/usersignup.html")


def otpverification(request, id, phone):
    if request.method == "POST":
        code = request.POST.get("otp")
        if verify.check(phone, code):
            user = CustomUser.objects.filter(id=id).update(is_verified=True)
            return redirect("userlogin")
        else:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return redirect("usersignup")

    return render(request, "userside/otpverification.html")


def mobilelogin(request):
    if request.method == "POST":
        phone = "+91" + request.POST.get("phone")
        user = CustomUser.objects.filter(phone=phone, is_verified=True)
        print(user)
        if user:
            try:
                verify.send(phone)
            except:
                return HttpResponse("Check your Internet Connection")
            return render(
                request, "userside/mobileotpverification.html", {"phone": phone}
            )
        else:
            messages.warning(
                request,
                "Phone number is not Registered,Please Enter the registered 10-digit Mobile Number",
            )
            return redirect("mobilelogin")

    return render(request, "userside/mobilelogin.html")


def mobileotpverification(request, phone):
    if request.method == "POST":
        code = request.POST.get("otp")
        if verify.check(phone, code):
            user = CustomUser.objects.get(phone=phone)
            if (
                user
                and user.is_user == True
                and user.is_active == True
                and user.is_verified == True
            ):
                login(request, user)
                return redirect("index")
            else:
                return redirect("usersignup")

    if request.user.is_authenticated:
        return render(request, "userside/index.html")
    else:
        return render(request, "userside/mobileotpverification.html")


def userlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if (
            user
            and user.is_user == True
            and user.is_active == True
            and user.is_verified == True
        ):
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid Credentails")
            return redirect("userlogin")

    if request.user.is_authenticated:
        return render(request, "userside/index.html")
    else:
        return render(request, "userside/userlogin.html")


def change_password_mobile(request):
    if request.method == "POST":
        phone = "+91" + request.POST.get("phone")
        if CustomUser.objects.filter(
            phone=phone, is_user=True, is_active=True, is_verified=True
        ):
            try:
                verify.send(phone)
            except:
                return HttpResponse("Check your Internet Connection")
            return render(
                request,
                "userside/change_password_otp_verification.html",
                {"phone": phone},
            )
        else:
            messages.warning(
                request,
                "Phone number is not Registered,Please Enter the registered 10-digit Mobile Number",
            )
            return redirect("change_password_mobile")

    return render(request, "userside/change_password_mobile.html")


def change_password_otp_verification(request, phone):
    if request.method == "POST":
        code = request.POST.get("otp")
        if verify.check(phone, code):
            user = CustomUser.objects.get(phone=phone)
            return redirect("change_password", id=user.id)
        else:
            messages.warning(request, "The otp you enterd is incorrect")
            return render(request, "userside/change_password_otp_verification.html")

    return render(request, "userside/change_password_otp_verification.html")


def change_password(request, id):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        if new_password == confirm_new_password:
            update_password = CustomUser.objects.filter(id=id).update(
                password=make_password(new_password)
            )
            messages.success(request, "Password changed succesfully,Please Login")
            return redirect("userlogin")
        else:
            messages.warning(
                request, "New password is not macthing with confirm new password"
            )
            return redirect("change_password")
    return render(request, "userside/change_password.html", {"user_id": id})


def userlogout(request):
    logout(request)
    return redirect("userlogin")


def productsdisplay(request, category):
    k = ProductDetails.objects.filter(product_category=category).order_by("productname")
    try:
        wishlist = Wishlist.objects.filter(user_id=request.user.id)
        wishlist_products = [item.product_name for item in wishlist]
        print(wishlist_products)
    except:
        pass
    return render(
        request,
        "userside/productsdisplay.html",
        {
            "s": k,
            "wishlist_products": wishlist_products,
            "category": category,
            "count": basket_count(request),
        },
    )


def productsfilter(request, category, filter_type):
    if filter_type == "price_low_to_high":
        k = ProductDetails.objects.filter(product_category=category).order_by(
            "unit_price"
        )
    else:
        k = ProductDetails.objects.filter(product_category=category).order_by(
            "-unit_price"
        )
    return render(
        request,
        "userside/productsdisplay.html",
        {"s": k, "category": category, "count": basket_count(request)},
    )


def viewproduct(request, id):
    k = ProductDetails.objects.get(id=id)
    return render(
        request, "userside/viewproduct.html", {"s": k, "count": basket_count(request)}
    )


def basket(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user_id=request.user.id)
        for item in basket:
            product = ProductDetails.objects.get(id=item.product_id)
            if item.quantity <= product.quantity:
                total = item.quantity * product.unit_price
                item.total = total
                item.unit_price = product.unit_price
                item.save()
            else:
                item.delete()

        result = Basket.objects.filter(user_id=request.user.id).aggregate(
            total=Sum("total")
        )
        if result["total"]:
            cart_total = result["total"]
        else:
            cart_total = 0
        # The result is returned as a dictionary, where the key 'total' corresponds to the alias you provided (total in this case). You can access the sum of numbers using the key 'total' or any other alias you specify.
        return render(
            request,
            "userside/basket.html",
            {"s": basket, "cart_total": cart_total, "count": basket_count(request)},
        )
    else:
        return render(request, "userside/userlogin.html")


def addtobasket(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            qty = int(request.POST.get("quantity"))
            k = ProductDetails.objects.get(id=id)
            item_exists = Basket.objects.filter(
                product_id=id, user_id=request.user.id
            )  # To check if the item exists
            if item_exists:
                cart_item = Basket.objects.get(
                    product_id=id, user_id=request.user.id
                )  # To check if the item exists
                remaining_qty = k.quantity - cart_item.quantity
                # this will check qty if item exists
                if qty <= remaining_qty:
                    update = Basket.objects.get(product_id=id, user_id=request.user.id)
                    update.quantity += qty
                    # update.total+=total
                    update.save()
                else:
                    messages.warning(
                        request, "Please,try a lesser quantity you have preached stock"
                    )

            else:
                # this will check qty if item does't exists
                if qty <= k.quantity:
                    b = Basket(
                        product_id=id,
                        product_name=k.productname,
                        quantity=qty,
                        unit_price=k.unit_price,
                        user_id=request.user.id,
                    )
                    b.img1 = k.img1
                    b.save()
                else:
                    messages.warning(
                        request, "Please,try a lesser quantity you have preached stock"
                    )

            return redirect("viewproduct", id=id)
        else:
            qty = 1
            k = ProductDetails.objects.get(id=id)
            item_exists = Basket.objects.filter(
                product_id=id, user_id=request.user.id
            )  # To check if the item exists
            if item_exists:
                cart_item = Basket.objects.get(
                    product_id=id, user_id=request.user.id
                )  # To check if the item exists
                remaining_qty = k.quantity - cart_item.quantity
                # this will check qty if item exists
                if qty <= remaining_qty:
                    update = Basket.objects.get(product_id=id, user_id=request.user.id)
                    update.quantity += qty
                    # update.total+=total
                    update.save()
                else:
                    messages.warning(
                        request, "Please,try a lesser quantity you have preached stock"
                    )

            else:
                # this will check qty if item does't exists
                if qty <= k.quantity:
                    b = Basket(
                        product_id=id,
                        product_name=k.productname,
                        quantity=qty,
                        unit_price=k.unit_price,
                        user_id=request.user.id,
                    )
                    b.img1 = k.img1
                    b.save()
                else:
                    messages.warning(
                        request, "Please,try a lesser quantity you have preached stock"
                    )

            return redirect("productsdisplay", category=k.product_category)
    else:
        return render(request, "userside/userlogin.html")


def removefrombasket(request, id):
    product = Basket.objects.filter(id=id, user_id=request.user.id)
    product.delete()
    return redirect("basket")


def basket_count(request):
    b = Basket.objects.filter(user_id=request.user.id)
    return b.count()


def youraddress(request):
    if request.user.is_authenticated:
        address = Address.objects.filter(user_id=request.user.id)
        if address.count() == 1:
            address.update(is_default=True)
        return render(
            request,
            "userside/address.html",
            {"address": address, "count": basket_count(request)},
        )
    else:
        return render(request, "userside/userlogin.html")


def yourprofile(request):
    if request.user.is_authenticated:
        return render(
            request, "userside/profile.html", {"count": basket_count(request)}
        )
    else:
        return render(request, "userside/userlogin.html")


def yourorders(request):
    if request.user.is_authenticated:
        orders = OrderDetails.objects.filter(user_id=request.user.id).order_by(
            "-date_and_time"
        )
        products = ProductDetails.objects.all()
        return render(
            request,
            "userside/orders.html",
            {"orders": orders, "count": basket_count(request), "products": products},
        )
    else:
        return render(request, "userside/userlogin.html")


def address_registration(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            full_name = request.POST.get("full_name")
            address_lane_1 = request.POST.get("address_lane_1")
            address_lane_2 = request.POST.get("address_lane_2")
            city_or_town = request.POST.get("city_or_town")
            district = request.POST.get("district")
            pincode = request.POST.get("pincode")
            phone_number = request.POST.get("phone_number")
            alt_phone_number = request.POST.get("alt_phone_number")
            land_mark = request.POST.get("land_mark")
            address = Address(
                user_id=request.user.id,
                full_name=full_name,
                address_lane_1=address_lane_1,
                address_lane_2=address_lane_2,
                city_or_town=city_or_town,
                district=district,
                pincode=pincode,
                phone_number=phone_number,
                alt_phone_number=alt_phone_number,
                land_mark=land_mark,
            )
            if Address.objects.filter(user_id=request.user.id):
                address.save()
            else:
                address.is_default = True
                address.save()
            return redirect("youraddress")

        return render(
            request,
            "userside/address_registration.html",
            {"count": basket_count(request)},
        )
    else:
        return render(request, "userside/userlogin.html")


def set_default(request, id):
    remove_default = Address.objects.filter(
        user_id=request.user.id, is_default=True
    ).update(is_default=False)
    set_default = Address.objects.filter(id=id, user_id=request.user.id).update(
        is_default=True
    )
    return redirect("youraddress")


def delete_address(request, id):
    address = Address.objects.get(id=id, user_id=request.user.id)
    if address.is_default == True:
        address.delete()
        set_another_default = Address.objects.filter(user_id=request.user.id)
        if set_another_default:
            set_another_default[0].is_default = True
            set_another_default[0].save()
    else:
        address.delete()
    return redirect("youraddress")


def update_address(request, id):
    if request.user.is_authenticated:
        address = Address.objects.get(id=id, user_id=request.user.id)
        template = loader.get_template("userside/address_updation.html")
        context = {"address": address, "count": basket_count(request)}
        return HttpResponse(template.render(context, request))
    else:
        return render(request, "userside/userlogin.html")


def address_updation(request, id):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address_lane_1 = request.POST.get("address_lane_1")
        address_lane_2 = request.POST.get("address_lane_2")
        city_or_town = request.POST.get("city_or_town")
        district = request.POST.get("district")
        pincode = request.POST.get("pincode")
        phone_number = request.POST.get("phone_number")
        alt_phone_number = request.POST.get("alt_phone_number")
        land_mark = request.POST.get("land_mark")
        address_update = Address.objects.filter(user_id=request.user.id, id=id).update(
            full_name=full_name,
            address_lane_1=address_lane_1,
            address_lane_2=address_lane_2,
            city_or_town=city_or_town,
            district=district,
            pincode=pincode,
            phone_number=phone_number,
            alt_phone_number=alt_phone_number,
            land_mark=land_mark,
        )
        return redirect("update_address", id=id)


def check_out(request, coupon_discount, coupon_id=0):
    if request.user.is_authenticated:
        k = Basket.objects.filter(user_id=request.user.id)
        try:
            coupon = Coupon.objects.get(id=coupon_id)
        except:
            coupon = None
        if k:
            address = Address.objects.filter(user_id=request.user.id, is_default=True)
            result = Basket.objects.filter(user_id=request.user.id).aggregate(
                total=Sum("total")
            )
            coupon_discount = float(coupon_discount)
            cart_total = result["total"] - coupon_discount
            return render(
                request,
                "userside/check_out.html",
                {
                    "address": address,
                    "count": basket_count(request),
                    "s": k,
                    "cart_total": float(result["total"]),
                    "final_cart_total": str(cart_total),
                    "coupon": coupon,
                    "coupon_discount": coupon_discount,
                    "coupon_id": coupon_id,
                },
            )
        else:
            return redirect("basket")
    else:
        return render(request, "userside/userlogin.html")


def apply_coupon(request, cart_total):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon")
        """try:
            coupon_id=Coupon.objects.get(coupon_code=coupon_code)
            if not UserCouponsApplied.objects.filter(user=request.user.id,coupon=coupon_id,is_applied=True):"""

        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code, is_disabled=False)
            result = Basket.objects.filter(user_id=request.user.id).aggregate(
                total=Sum("total")
            )
            if coupon.coupon_type == "percentage_off":
                coupon_discount = (float(result["total"]) * coupon.discount) / 100
            else:
                coupon_discount = coupon.discount
            user = CustomUser.objects.get(id=request.user.id)
            coupon_apply = UserCouponsApplied.objects.create(
                user=user, coupon=coupon, is_applied=True
            )
            return redirect(
                "check_out", coupon_discount=str(coupon_discount), coupon_id=coupon.id
            )
        except:
            messages.warning(request, "Enter a valid coupon id")
            return redirect("check_out", coupon_discount="0", coupon_id=0)

        """else:
                messages.warning(request,"This coupon is already used by the you ")
                return redirect('check_out',coupon_discount='0')
        except:
            messages.warning(request,"Enter a valid coupon id")
            return redirect('check_out',coupon_discount='0')"""


# Generate a unique identifier: To generate a unique identifier for the orders placed at once, you can use the uuid module in Python.
# This module provides functions to create universally unique identifiers (UUIDs).


def generate_bunch_order_id():
    return str(uuid.uuid4())


def place_and_pay(request, amount, coupon_id):
    if request.method == "POST":
        amount = float(amount)
        address = request.POST.get("address")
        payment = request.POST.get("payment")
        bunch_order_id = generate_bunch_order_id()
        if payment == "cod":
            items = Basket.objects.filter(user_id=request.user.id)
            for item in items:
                product = ProductDetails.objects.get(id=item.product_id)
                vendor_id = product.vendor_id
                order = OrderDetails(
                    bunch_order_id=bunch_order_id,
                    product_id=item.product_id,
                    product_name=product.productname,
                    product_image=product.img1,
                    user_id=request.user.id,
                    address_id=address,
                    unit_price=product.unit_price,
                    vendor_id=vendor_id,
                    quantity=item.quantity,
                    amount=item.total,
                    bunch_order_amount=amount,
                    payment_type=payment,
                    order_status="Received",
                    date_and_time=timezone.now(),
                    coupon_id=coupon_id,
                )
                order.save()
                newqty = product.quantity - item.quantity
                update_quantity = ProductDetails.objects.filter(
                    id=item.product_id
                ).update(quantity=newqty)
            items.delete()
            return redirect("order_success", order_id=bunch_order_id)
        if payment == "razorpay":
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create(
                {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
            )
            prepaid_order = PrePaidOrder.objects.create(
                order_id=bunch_order_id,
                amount=amount,
                provider_order_id=razorpay_order["id"],
            )
            items = Basket.objects.filter(user_id=request.user.id)
            for item in items:
                product = ProductDetails.objects.get(id=item.product_id)
                vendor_id = product.vendor_id
                order = OrderDetails(
                    bunch_order_id=bunch_order_id,
                    product_id=item.product_id,
                    product_name=product.productname,
                    product_image=product.img1,
                    user_id=request.user.id,
                    address_id=address,
                    unit_price=product.unit_price,
                    vendor_id=vendor_id,
                    quantity=item.quantity,
                    amount=item.total,
                    bunch_order_amount=amount,
                    payment_type=payment,
                    order_status="Received",
                    date_and_time=timezone.now(),
                    coupon_id=coupon_id,
                )
                order.save()
                prepaid_order.save()
                newqty = product.quantity - item.quantity
                update_quantity = ProductDetails.objects.filter(
                    id=item.product_id
                ).update(quantity=newqty)
            items.delete()
            return render(
                request,
                "userside/place_and_pay.html",
                {
                    "callback_url": "http://" + "127.0.0.1:8000" + "/callback/",
                    "razorpay_key": RAZORPAY_KEY_ID,
                    "order": prepaid_order,
                },
            )

    return render(request, "userside/place_and_pay.html")


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = PrePaidOrder.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()

        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            payment_update = OrderDetails.objects.filter(
                bunch_order_id=order.order_id
            ).update(payment_status="Paid")
            order.save()
            return redirect("order_success", order_id=order.order_id)
        else:
            order.status = PaymentStatus.FAILURE
            payment_fail_orders_delete = OrderDetails.objects.filter(
                bunch_order_id=order.order_id
            ).delete()
            order.save()
            return render(request, "userside/order_failed.html")
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = PrePaidOrder.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        payment_fail_orders_delete = OrderDetails.objects.filter(
            bunch_order_id=order.order_id
        ).delete()
        order.save()
        return render(request, "userside/order_failed.html")


def order_success(request, order_id):
    orders = OrderDetails.objects.filter(bunch_order_id=order_id)
    address = Address.objects.get(id=orders[0].address_id)
    date = orders[0].date_and_time.date()
    sub_total = OrderDetails.objects.filter(bunch_order_id=order_id).aggregate(
        total=Sum("amount")
    )
    discount = sub_total["total"] - orders[0].bunch_order_amount
    total_amount = orders[0].bunch_order_amount
    return render(
        request,
        "userside/order_success.html",
        {
            "orders": orders,
            "bunch_order_id": order_id,
            "count": basket_count(request),
            "total_amount": total_amount,
            "address": address,
            "sub_total": sub_total["total"],
            "date": date,
            "discount": discount,
        },
    )


def order_failure(request):
    return render(
        request, "userside/order_failed.html", {"count": basket_count(request)}
    )


def user_cancel_order(request, id):
    canceled_order = OrderDetails.objects.get(id=id)
    product = ProductDetails.objects.get(id=canceled_order.product_id)
    product.quantity += canceled_order.quantity
    product.save()
    stock_updation = OrderDetails.objects.filter(id=id, user_id=request.user.id).update(
        order_status="Canceled", is_canceled=True
    )
    return redirect("yourorders")


def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user_id=request.user.id)
        return render(
            request,
            "userside/wishlist.html",
            {"wishlist": wishlist, "count": basket_count(request)},
        )
    else:
        return render(request, "userside/userlogin.html")


def add_to_wishlist(request, id):
    if request.user.is_authenticated:
        product = ProductDetails.objects.get(id=id)
        item_exists = Wishlist.objects.filter(product_id=id, user_id=request.user.id)
        if item_exists:
            messages.warning(request, "Product already in wishlist")
            return redirect("productsdisplay", category=product.product_category)
        else:
            add_to_wishlist = Wishlist(
                user_id=request.user.id,
                product_id=id,
                product_name=product.productname,
                img1=product.img1,
                listed=True,
            )
            product.is_listed = True
            add_to_wishlist.save()
            product.save()
            # messages.success(request,product.productname+",added to wishlist")
            return redirect("productsdisplay", category=product.product_category)
    else:
        return render(request, "userside/userlogin.html")


def remove_from_wishlist(request, id):
    if request.user.is_authenticated:
        item = Wishlist.objects.filter(product_id=id, user_id=request.user.id)
        update_product_listed = ProductDetails.objects.filter(id=id).update(
            is_listed=False
        )
        item.delete()
        return redirect("wishlist")
    else:
        return render(request, "userside/userlogin.html")


def user_view_order(request, bunch_order_id):
    if request.user.is_authenticated:
        orders = OrderDetails.objects.filter(bunch_order_id=bunch_order_id)
        sub_total = OrderDetails.objects.filter(
            bunch_order_id=bunch_order_id, is_canceled=False
        ).aggregate(total=Sum("amount"))
        bunch_order_amount = orders[0].bunch_order_amount
        order_date = orders[0].date_and_time
        try:
            coupon = Coupon.objects.get(id=orders[0].coupon_id)
            coupon_discount = sub_total["total"] - bunch_order_amount
        except:
            coupon = None
            coupon_discount = 0

        return render(
            request,
            "userside/view_order.html",
            {
                "bunch_order_id": bunch_order_id,
                "orders": orders,
                "count": basket_count(request),
                "sub_total": sub_total["total"],
                "bunch_order_amount": bunch_order_amount,
                "coupon": coupon,
                "coupon_discount": coupon_discount,
                "order_date": order_date,
            },
        )
    else:
        return render(request, "userside/userlogin.html")
