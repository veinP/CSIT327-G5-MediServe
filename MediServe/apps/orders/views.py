from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.medicine.models import Medicine
from .models import Order, OrderItem

# 🟢 Add medicine to order
@login_required
def add_to_order(request, medicine_id):
    """Add a medicine to the user's active order (no pricing involved)."""
    medicine = get_object_or_404(Medicine, id=medicine_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        special_request = request.POST.get("special_request", "")

        if quantity > medicine.stock_quantity:
            messages.warning(request, f"⚠️ Only {medicine.stock_quantity} available in stock.")
            return redirect("medicine_info", medicine_id=medicine.id)

        # Create or get a pending order
        order, created = Order.objects.get_or_create(
            user=request.user,
            status="Pending",
            defaults={"created_at": timezone.now()}
        )

        # Create or update order item
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

        messages.success(request, f"✅ Added {quantity} × {medicine.name} to your order.")
        return redirect("order_list")

    return redirect("medicine_info", medicine_id=medicine.id)


# 🟢 View all orders (no price)
@login_required
def order_list(request):
    try:
        order = Order.objects.get(user=request.user, status="Pending")
        items = order.items.all()
    except Order.DoesNotExist:
        items = []

    context = {"items": items}
    return render(request, "order_list.html", context)


# 🟢 Admin: Manage delivery (reduces stock on “ship”)
@login_required
def delivery_page(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        action = request.POST.get("action")
        order = get_object_or_404(Order, id=order_id)

        # When admin ships the order
        if action == "ship":
            for item in order.items.all():
                medicine = item.medicine

                # Check stock before reducing
                if medicine.stock_quantity >= item.quantity:
                    medicine.stock_quantity -= item.quantity
                    medicine.save()
                else:
                    messages.warning(
                        request,
                        f"⚠️ Not enough stock for {medicine.name}. "
                        f"Available: {medicine.stock_quantity}, Needed: {item.quantity}"
                    )
                    return redirect("delivery_page")

            order.status = "Shipped"
            order.save()
            messages.success(request, f"🚚 Order #{order.id} marked as shipped and stock updated!")

        # When admin completes the order
        elif action == "complete":
            order.status = "Completed"
            order.save()
            messages.success(request, f"✅ Order #{order.id} marked as completed!")

        return redirect("delivery_page")

    # Show active orders
    orders = Order.objects.exclude(status="Completed").order_by("-created_at")
    return render(request, "delivery_page.html", {"orders": orders})


# 🟢 Remove item from order
@login_required
def remove_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    item.delete()
    messages.success(request, "🗑️ Item removed from your order.")
    return redirect("order_list")


# 🟢 Simple checkout confirmation
@login_required
def order_checkout(request):
    return render(request, "order_checkout.html")
