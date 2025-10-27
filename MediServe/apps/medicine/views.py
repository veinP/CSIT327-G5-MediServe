from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from supabase import create_client
from .models import Medicine
from .forms import MedicineForm

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


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
    """Edit medicine both in local DB and Supabase."""
    local_medicine = Medicine.objects.filter(id=id).first()

    # Get from Supabase
    response = supabase.table("tblmedicine").select("*").eq("id", id).single().execute()
    medicine_data = response.data

    if not medicine_data:
        messages.error(request, "⚠️ Medicine not found.")
        return redirect('medicine_stock')

    if request.method == 'POST':
        stock_quantity = request.POST.get("stock_quantity")
        price = request.POST.get("price")
        description = request.POST.get("description")

        # Update Supabase
        update = supabase.table("tblmedicine").update({
            "stock_quantity": stock_quantity,
            "price": price,
            "description": description
        }).eq("id", id).execute()

        if update.data:
            if local_medicine:
                local_medicine.stock_quantity = stock_quantity
                local_medicine.price = price
                local_medicine.description = description
                local_medicine.save()

            messages.success(request, f"✅ {medicine_data['name']} updated successfully!")
        else:
            messages.error(request, "⚠️ Failed to update medicine. Please try again.")

        return redirect('medicine_stock')

    return render(request, 'edit_medicine.html', {'medicine': medicine_data})


# -------------------------------------------------------------------
# Delete Medicine (Instant Delete, No Confirmation Page)
# -------------------------------------------------------------------
@login_required
def delete_medicine(request, id):
    """Delete medicine directly (both local and Supabase)."""
    if request.method == "POST":
        try:
            # 1️⃣ Delete from Supabase
            supabase.table("tblmedicine").delete().eq("id", id).execute()

            # 2️⃣ Delete from local DB (if exists)
            local_medicine = Medicine.objects.filter(id=id).first()
            if local_medicine:
                local_medicine.delete()

            messages.success(request, "🗑️ Medicine deleted successfully!")
        except Exception as e:
            messages.error(request, f"⚠️ Error deleting medicine: {e}")

    return redirect("medicine_stock")


# -------------------------------------------------------------------
# Public Browse Page (Supabase only)
# -------------------------------------------------------------------
def medicine_list(request):
    """Public Browse Medicines page."""
    response = supabase.table("tblmedicine").select("*").execute()
    medicines = response.data if response.data else []
    medicines = sorted(medicines, key=lambda x: x.get('name', '').lower())

    return render(request, 'medicine_list.html', {'medicines': medicines})


# -------------------------------------------------------------------
# Medicine Info Page
# -------------------------------------------------------------------
def medicine_info(request, medicine_id):
    """Medicine details page."""
    response = supabase.table("tblmedicine").select("*").eq("id", medicine_id).single().execute()
    medicine = response.data

    if not medicine:
        messages.error(request, "⚠️ Medicine not found.")
        return redirect("medicine_stock")

    return render(request, 'medicine_info.html', {'medicine': medicine})
