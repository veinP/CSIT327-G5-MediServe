from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine
from .forms import MedicineForm


# -------------------------------------------------------------------
# Medicine History Page
# -------------------------------------------------------------------
@login_required
def medicine_history(request):
    return render(request, 'medicine_history.html')


# -------------------------------------------------------------------
# Admin: Medicine Stock (Main CRUD Page)
# -------------------------------------------------------------------
@login_required
def medicine_stock(request):
    """Medicine stock management (admin view)."""
    medicines = Medicine.objects.all().order_by('name')

    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Medicine added successfully!')
            return redirect('medicine_stock')
        else:
            messages.error(request, '⚠️ Please correct the errors below.')
    else:
        form = MedicineForm()

    return render(request, 'medicine_stock.html', {
        'medicines': medicines,
        'form': form,
    })


# -------------------------------------------------------------------
# Medicine Records Page (if needed separately)
# -------------------------------------------------------------------
@login_required
def medicine_records(request):
    return render(request, 'medicine_records.html')


# -------------------------------------------------------------------
# Edit Medicine
# -------------------------------------------------------------------
@login_required
def edit_medicine(request, id):
    """Edit medicine details."""
    medicine = get_object_or_404(Medicine, id=id)

    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, f"✅ {medicine.name} updated successfully!")
            return redirect('medicine_stock')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = MedicineForm(instance=medicine)

    return render(request, 'edit_medicine.html', {
        'form': form,
        'medicine': medicine,
    })


# -------------------------------------------------------------------
# Delete Medicine (Instant Delete, No Confirmation Page)
# -------------------------------------------------------------------
@login_required
def delete_medicine(request, id):
    """Delete medicine directly from local DB."""
    if request.method == "POST":
        try:
            medicine = Medicine.objects.get(id=id)
            medicine_name = medicine.name
            medicine.delete()
            messages.success(request, f"🗑️ {medicine_name} deleted successfully!")
        except Medicine.DoesNotExist:
            messages.error(request, "⚠️ Medicine not found.")
        except Exception as e:
            messages.error(request, f"⚠️ Error deleting medicine: {e}")

    return redirect("medicine_stock")


# -------------------------------------------------------------------
# Public Browse Page
# -------------------------------------------------------------------
def medicine_list(request):
    """Public Browse Medicines page."""
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'medicine_list.html', {'medicines': medicines})


# -------------------------------------------------------------------
# Medicine Info Page
# -------------------------------------------------------------------
def medicine_info(request, medicine_id):
    """Medicine details page."""
    medicine = get_object_or_404(Medicine, id=medicine_id)
    return render(request, 'medicine_info.html', {'medicine': medicine})
