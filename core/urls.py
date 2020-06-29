from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('feed', views.feed, name='feed'),
    path('store', views.store, name='store'),

    path('product/<slug>', views.product, name='product'),
    path('vendor/<slug>', views.vendor, name='vendor'),

    path('search', views.search, name = 'search'),
    path('search_more', views.search_more, name = 'search_more'),

    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
    path('request-refund/', views.RequestRefundView.as_view(), name='request-refund'),
 
    path('drivers/', views.drivers, name='drivers'),
    path('order/<ref_code>', views.OrderView.as_view(), name='order'),
    path('set-driver/<ref_code>', views.set_driver, name='set-driver'),
    path('account/', views.account, name='account'),
    path('account/<str:page>', views.account_page, name='account_page'),
]