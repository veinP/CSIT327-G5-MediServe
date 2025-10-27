# MediServe/urls.py
from django.contrib import admin
from django.urls import path, include
from apps.accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🏠 Redirect root to login page first
    path('', views.home_redirect, name='home_redirect'),

    # 🧭 Main navigation pages
    path('main_menu/', views.main_menu_view, name='main_menu'),
    path('admin_menu/', views.admin_menu_view, name='admin_menu'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_page, name='settings'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('announcements/', include('apps.announcements.urls')),


    # 📦 Include app routes
    path('accounts/', include('apps.accounts.urls')),
    path('medicine/', include('apps.medicine.urls')),
    path('orders/', include('apps.orders.urls')),
    path('announcements/', include('apps.announcements.urls')),
    path('analytics/', include('apps.analytics.urls')),
]
