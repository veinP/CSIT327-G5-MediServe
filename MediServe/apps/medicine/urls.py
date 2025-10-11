from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('history/', views.medicine_history, name='medicine_history'),
    path('stock/', views.medicine_stock, name='medicine_stock'),  # ✅ Add this line
    path('records/', views.medicine_records, name='medicine_records'),  # ✅ added
]
