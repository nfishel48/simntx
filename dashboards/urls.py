from django.urls import path

from . import views

app_name = 'dashboards'

urlpatterns = [
    path('vendor/', views.vendor, name = 'vendor'),
    path('vendor/order/<str:ref_code>', views.vendor_order, name = 'vendor_order'),
    path('vendor/past_orders/<str:month>', views.vendor_past_month, name = 'vendor_past_month'),
    path('vendor/order_action', views.order_action, name = 'order_action'),
    path('vendor/<str:page>', views.vendor_page, name='vendor_page'),
    path('vendor/<str:page>/edit/<int:id>', views.edit_page, name='edit_page'),
    path('vendor/<str:page>/create', views.create_page, name='create_page'),
    path('vendor/<str:page>/delete/<slug:id>', views.delete_page, name='delete_page'),
    path('vendor/<str:page>/delete/<slug:id>', views.delete_page, name='delete_page'),

    path('vendor/approve-order/<ref_code>', views.approve_order, name='approve-order'),
    path('vendor/deny-order/<ref_code>', views.deny_order, name='deny-order'),

    path('driver', views.driver, name = 'driver'),
    path('driver/<str:page>', views.driver_page, name = 'driver_page'),
    path('driver/order/<str:ref_code>', views.order, name = 'order'),

    path('set-driver/<ref_code>', views.set_driver, name='set-driver'),
    path('set-delivered/<ref_code>', views.set_delivered, name='set_delivered'),
    path('unset-driver/<ref_code>', views.unset_driver, name='unset_driver'),
    path('cancel-order/<ref_code>', views.cancel_order, name='cancel_order'),

    path('admin', views.admin, name='admin'),
    path('admin/<str:page>', views.admin_page, name='admin_page'),
    path('admin/past_months/<str:month>', views.admin_past_month, name = 'admin_past_month'),
]