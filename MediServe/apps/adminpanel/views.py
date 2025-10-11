from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def admin_menu_view(request):
    # You can add logic here for admin dashboard
    return render(request, 'admin_menu.html')