from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Medicine
from .forms import MedicineForm
from django.contrib import messages
from supabase import create_client
from django.conf import settings

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


def medicine_list(request):
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    # Fetch all medicines
    response = supabase.table("tblmedicine").select("*").execute()
    medicines = response.data if response.data else []

    # Optional: sort or filter before sending to template
    medicines = sorted(medicines, key=lambda x: x.get('name', '').lower())

    return render(request, 'medicine_list.html', {
        'medicines': medicines
    })

def medicine_info(request, medicine_id):
    from .models import Medicine
    medicine = Medicine.objects.get(id=medicine_id)
    return render(request, 'medicine_info.html', {'medicine': medicine})


