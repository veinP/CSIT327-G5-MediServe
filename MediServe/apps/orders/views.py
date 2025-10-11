from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def order_list(request):
    return render(request, 'order_list.html')

def delivery_page(request):
    return render(request, 'user_delivery_view.html')