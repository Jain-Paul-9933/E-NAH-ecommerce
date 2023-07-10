"""
URL configuration for enah project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from userside import views

urlpatterns = [
    path("", views.index, name="index"),
    path("usersignup", views.usersignup, name="usersignup"),
    path("userlogin", views.userlogin, name="userlogin"),
    path("userlogout", views.userlogout, name="userlogout"),
    path(
        "productsdisplay/<str:category>", views.productsdisplay, name="productsdisplay"
    ),
    path(
        "productsfilter/<str:category>,<str:filter_type>",
        views.productsfilter,
        name="productsfilter",
    ),
    path("viewproduct/<int:id>", views.viewproduct, name="viewproduct"),
    path(
        "otpverification/<int:id>,<str:phone>",
        views.otpverification,
        name="otpverification",
    ),
    path("mobilelogin", views.mobilelogin, name="mobilelogin"),
    path(
        "mobileotpverification/<str:phone>",
        views.mobileotpverification,
        name="mobileotpverification",
    ),
    path(
        "change_password_mobile",
        views.change_password_mobile,
        name="change_password_mobile",
    ),
    path(
        "change_password_otp_verification/<str:phone>",
        views.change_password_otp_verification,
        name="change_password_otp_verification",
    ),
    path("change_password/<int:id>", views.change_password, name="change_password"),
    path("basket", views.basket, name="basket"),
    path("addtobasket/<int:id>", views.addtobasket, name="addtobasket"),
    path("removefrombasket/<int:id>", views.removefrombasket, name="removefrombasket"),
    path("youraddress", views.youraddress, name="youraddress"),
    path("yourprofile", views.yourprofile, name="yourprofile"),
    path("yourorders", views.yourorders, name="yourorders"),
    path(
        "address_registration", views.address_registration, name="address_registration"
    ),
    path("set_default/<int:id>", views.set_default, name="set_default"),
    path("update_address/<int:id>", views.update_address, name="update_address"),
    path("delete_address/<int:id>", views.delete_address, name="delete_address"),
    path("address_updation/<int:id>", views.address_updation, name="address_updation"),
    path(
        "check_out/<str:coupon_discount>,<int:coupon_id>",
        views.check_out,
        name="check_out",
    ),
    path(
        "place_and_pay/<str:amount>,<int:coupon_id>",
        views.place_and_pay,
        name="place_and_pay",
    ),
    path("callback/", views.callback, name="callback"),
    path("order_success/<str:order_id>", views.order_success, name="order_success"),
    path("order_failure", views.order_failure, name="order_failure"),
    path(
        "user_cancel_order/<int:id>", views.user_cancel_order, name="user_cancel_order"
    ),
    path(
        "user_view_order/<str:bunch_order_id>",
        views.user_view_order,
        name="user_view_order",
    ),
    path("wishlist", views.wishlist, name="wishlist"),
    path("add_to_wishlist/<int:id>", views.add_to_wishlist, name="add_to_wishlist"),
    path(
        "remove_from_wishlist/<int:id>",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),
    path("apply_coupon/<str:cart_total>", views.apply_coupon, name="apply_coupon"),
]
