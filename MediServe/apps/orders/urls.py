from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('delivery/', views.delivery_page, name='delivery_page'),
    path('add-to-order/<int:medicine_id>/', views.add_to_order, name='add_to_order'),
]
