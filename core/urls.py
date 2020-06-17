from django.urls import path
from .views import (
    ItemDetailView,
    TestItemDetailView,
    CheckoutView,
    ShopView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    VendorView,
    TestVendorView,
    VendorDetailView,
    vendorShop,
    drivers
)
from . import views

app_name = 'core'

urlpatterns = [
    path('shop/', ShopView.as_view(), name='shop'),

    path('', VendorView.as_view(), name='home'),
    path('test', TestVendorView.as_view(), name='test_home'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),

    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('test/product/<slug>/', TestItemDetailView.as_view(), name='test_product'),
    path('vendor_page/<slug>/', VendorDetailView.as_view(), name='vendor_page'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('vendor_shop/<owner>/', vendorShop, name='vendor-shop'),
    path('drivers/', drivers, name='drivers'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('test', views.index, name='index'),
    path('test/product/<slug>/', views.TestItemDetailView.as_view(), name='test_product'),
    path('test/vendor/<slug>/', views.TestVendorDetailView.as_view(), name='test_vendor_page')
   
]
