from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def medicine_list(request):
    return render(request, 'medicine_list.html')

@login_required
def medicine_history(request):
    return render(request, 'medicine_history.html')

def medicine_stock(request):
    return render(request, 'medicine_stock.html')

def medicine_records(request):
    return render(request, 'medicine_records.html')
