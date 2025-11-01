from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add-to-order/<int:medicine_id>/', views.add_to_order, name='add_to_order'),
    path('delivery/', views.delivery_page, name='delivery_page'),
    path("remove/<int:item_id>/", views.remove_order_item, name="remove_order_item"),
    path('checkout/', views.order_checkout, name='order_checkout'),

]
