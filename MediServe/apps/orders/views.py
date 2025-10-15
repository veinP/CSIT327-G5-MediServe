from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from apps.medicine.models import Medicine
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required
def order_list(request):
    return render(request, 'order_list.html')

def delivery_page(request):
    return render(request, 'user_delivery_view.html')

def add_to_order(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    if request.method == "POST":
        quantity = int(request.POST.get("amount", 1))
        special_request = request.POST.get("special_request", "")

        # Create or get an active "Pending" order for the user
        order, created = Order.objects.get_or_create(
            user=request.user,
            status="Pending",
            defaults={"created_at": timezone.now(), "total_price": 0}
        )

        # Add or update this medicine in the order
        item, item_created = OrderItem.objects.get_or_create(
            order=order,
            medicine=medicine,
            defaults={"quantity": quantity, "special_request": special_request}
        )

        if not item_created:
            item.quantity += quantity
            if special_request:
                item.special_request = special_request
            item.save()

        # Update total
        order.total_price = sum(i.get_total_price() for i in order.items.all())
        order.save()

        messages.success(request, f"Added {quantity} × {medicine.name} to your order.")

        # Redirect to a confirmation or medicine list page
        return redirect('medicine_list')  # you can change this

    return redirect('medicine_info', medicine_id=medicine.id)
