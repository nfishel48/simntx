from django.urls import path
from . import views

app_name = 'vendor'

urlpatterns = [
    path('', views.index, name='index'),
]