from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcements_view, name='announcements'),
]
