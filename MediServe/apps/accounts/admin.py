from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "gender", "role", "date_of_birth", "created_at")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("gender", "role", "created_at")
