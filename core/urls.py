from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('shop/', views.ShopView.as_view(), name='shop'),

    path('', views.VendorView.as_view(), name='home'),
    path('test', views.index, name='index'),

    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),

    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('test/product/<slug>/', views.TestItemDetailView.as_view(), name='test_product'),

    path('vendor_page/<slug>/', views.VendorDetailView.as_view(), name='vendor_page'),
    path('test/vendor/<slug>/', views.TestVendorDetailView.as_view(), name='test_vendor_page'),

    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
    path('request-refund/', views.RequestRefundView.as_view(), name='request-refund'),

    path('vendor_shop/<owner>/', views.vendorShop, name='vendor-shop')
]
