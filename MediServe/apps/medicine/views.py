from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine
from .forms import MedicineForm
from supabase import create_client
from django.conf import settings

@login_required
def medicine_history(request):
    return render(request, 'medicine_history.html')

@login_required
def medicine_stock(request):
    medicines = Medicine.objects.all().order_by('name')

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

@login_required
def edit_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    form = MedicineForm(request.POST or None, instance=medicine)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f"{medicine.name} updated successfully!")
            return redirect('medicine_stock')

    return render(request, 'edit_medicine.html', {
        'form': form,
        'medicine': medicine,
    })

@login_required
def delete_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    medicine.delete()
    messages.success(request, f"{medicine.name} deleted successfully.")
    return redirect('medicine_stock')

def medicine_list(request):
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    response = supabase.table("tblmedicine").select("*").execute()
    medicines = response.data if response.data else []
    medicines = sorted(medicines, key=lambda x: x.get('name', '').lower())

    return render(request, 'medicine_list.html', {'medicines': medicines})

def medicine_info(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    return render(request, 'medicine_info.html', {'medicine': medicine})
