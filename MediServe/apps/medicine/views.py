from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Medicine
from .forms import MedicineForm
from django.contrib import messages

@login_required
def medicine_list(request):
    return render(request, 'medicine_list.html')

@login_required
def medicine_history(request):
    return render(request, 'medicine_history.html')

@login_required
def medicine_stock(request):
    medicines = Medicine.objects.all().order_by('name')

    # Handle form submission (Add Medicine)
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine added successfully!')
            return redirect('medicine_stock')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MedicineForm()

    return render(request, 'medicine_stock.html', {
        'medicines': medicines,
        'form': form,
    })

@login_required
def medicine_records(request):
    return render(request, 'medicine_records.html')

def edit_medicine(request, id):
    # fetch medicine by id and show a pre-filled form
    pass

def delete_medicine(request, id):
    # delete medicine and redirect with a message
    pass

