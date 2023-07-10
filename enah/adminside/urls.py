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
from adminside import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("adminhome", views.adminhome, name="adminhome"),
    path("vendor_registration", views.vendor_registration, name="vendor_registration"),
    path("adminlogin", views.adminlogin, name="adminlogin"),
    path("userslist", views.userslist, name="userslist"),
    path("vendorslist", views.vendorslist, name="vendorslist"),
    path("adminlogout", views.adminlogout, name="adminlogout"),
    path("adminproductslist", views.adminproductslist, name="adminproductslist"),
    path("viewuser/<int:id>", views.viewuser, name="viewuser"),
    path("viewvendor/<int:id>", views.viewvendor, name="viewvendor"),
    path("blockuser/<int:id>", views.blockuser, name="blockuser"),
    path("unblockuser/<int:id>", views.unblockuser, name="unblockuser"),
    path("updatevendor/<int:id>", views.updatevendor, name="updatevendor"),
    path("vendor_updation/<int:id>", views.vendor_updation, name="vendor_updation"),
    path("admin_order_list", views.admin_order_list, name="admin_order_list"),
    path(
        "admin_cancel_order/<int:id>",
        views.admin_cancel_order,
        name="admin_cancel_order",
    ),
    path("adminvieworder/<int:id>", views.adminvieworder, name="adminvieworder"),
    path(
        "admin_order_status_listing/<str:status>",
        views.admin_order_status_listing,
        name="admin_order_status_listing",
    ),
    path("accounts", views.accounts, name="accounts"),
    path(
        "notify_vendor/<int:vendor_id>,<int:id>,<str:productname>",
        views.notify_vendor,
        name="notify_vendor",
    ),
    path("admin_coupon_list", views.admin_coupon_list, name="admin_coupon_list"),
    path("sales_report", views.sales_report, name="sales_report"),
    path("coupon_registration", views.coupon_registration, name="coupon_registration"),
    path(
        "disable_enable_coupon/<int:id>",
        views.disable_enable_coupon,
        name="disable_enable_coupon",
    ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
