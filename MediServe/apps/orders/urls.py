from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('delivery/', views.delivery_page, name='delivery_page'),
]
