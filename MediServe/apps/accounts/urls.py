from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_menu/', views.admin_menu_view, name='admin_menu'),
    path('main_menu/', views.main_menu_view, name='main_menu'),
    path('profile/', views.profile_view, name='profile_view'),
]
