from django.urls import path

from . import views

app_name = 'dashboards'

urlpatterns = [
    path('vendor/', views.vendor, name = 'vendor'),
    path('vendor/order/<str:ref_code>', views.vendor_order, name = 'vendor_order'),
    path('vendor/past_orders/<str:month>', views.vendor_past_month, name = 'vendor_past_month'),
    path('vendor/<str:page>', views.vendor_page, name='vendor_page'),
    path('vendor/<str:page>/edit/<int:id>', views.edit_page, name='edit_page'),
    path('vendor/<str:page>/create', views.create_page, name='create_page'),
    path('vendor/<str:page>/delete/<slug:id>', views.delete_page, name='delete_page'),

    path('driver', views.driver, name = 'driver'),
    path('driver/<str:page>', views.driver_page, name = 'driver_page'),
    path('driver/order/<str:ref_code>', views.order, name = 'order'),
]