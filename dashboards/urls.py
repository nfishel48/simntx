from django.urls import path

from . import views

app_name = 'dashboards'

urlpatterns = [
    path('vendor/', views.vendor, name = 'vendor'),
    path('vendor/<str:page>', views.vendor_page, name='vendor_page'),
    path('vendor/<str:page>/edit/<int:id>', views.edit_page, name='edit_page'),
    path('vendor/<str:page>/create', views.create_page, name='create_page'),
    path('vendor/<str:page>/delete/<int:id>', views.delete_page, name='delete_page'),

    path('driver', views.driver, name = 'driver'),
    path('driver/<str:page>', views.driver_page, name = 'driver_page'),
    path('driver/order/<str:ref_code>', views.order, name = 'order'),
]