from django.urls import path
from . import views

urlpatterns = [
    # User-facing pages
    path('browse-medicines/', views.medicine_list, name='medicine_list'),
    path('<int:medicine_id>/', views.medicine_info, name='medicine_info'),

    # Admin pages
    path('admin/medicine-stock/', views.medicine_stock, name='medicine_stock'),
    path('records/', views.medicine_records, name='medicine_records'),
    path('edit/<int:id>/', views.edit_medicine, name='edit_medicine'),
    path('delete/<int:id>/', views.delete_medicine, name='delete_medicine'),

    # History
    path('history/', views.medicine_history, name='medicine_history'),
]
