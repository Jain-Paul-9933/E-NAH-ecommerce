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
from vendorside import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("vendorhome", views.vendorhome, name="vendorhome"),
    path(
        "product_registration", views.product_registration, name="product_registration"
    ),
    path("vendorlogin", views.vendorlogin, name="vendorlogin"),
    path("vendorlogout", views.vendorlogout, name="vendorlogout"),
    path("productslist", views.productslist, name="productslist"),
    path(
        "vendorviewproduct/<int:id>", views.vendorviewproduct, name="vendorviewproduct"
    ),
    path("blockproduct/<int:id>", views.blockproduct, name="blockproduct"),
    path("unblockproduct/<int:id>", views.unblockproduct, name="unblockproduct"),
    path("updateproduct/<int:id>", views.updateproduct, name="updateproduct"),
    path("product_updation/<int:id>", views.product_updation, name="product_updation"),
    path("order_list", views.order_list, name="order_list"),
    path("accept_order/<int:id>", views.accept_order, name="accept_order"),
    path("pack_order/<int:id>", views.pack_order, name="pack_order"),
    path("ship_order/<int:id>", views.ship_order, name="ship_order"),
    path("deliverd_order/<int:id>", views.deliverd_order, name="deliverd_order"),
    path("cancel_order/<int:id>", views.cancel_order, name="cancel_order"),
    path("close_order/<int:id>", views.close_order, name="close_order"),
    path(
        "order_status_listing/<str:status>",
        views.order_status_listing,
        name="order_status_listing",
    ),
    path(
        "update_status_all/<str:status>",
        views.update_status_all,
        name="update_status_all",
    ),
    path("vendorvieworder/<int:id>", views.vendorvieworder, name="vendorvieworder"),
    path("stock", views.stock, name="stock"),
    path("update_stock/<int:id>", views.update_stock, name="update_stock"),
    path(
        "delete_notification/<int:id>",
        views.delete_notification,
        name="delete_notification",
    ),
    path("coupon_list", views.coupon_list, name="coupon_list"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
