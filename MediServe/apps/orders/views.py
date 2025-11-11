from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from apps.medicine.models import Medicine
from .models import Order, OrderItem

User = get_user_model()


# 🟢 Add medicine to order
@login_required
def add_to_order(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        special_request = request.POST.get("special_request", "")

        if quantity > medicine.stock_quantity:
            messages.warning(request, f"⚠️ Only {medicine.stock_quantity} available in stock.")
            return redirect("medicine_info", medicine_id=medicine.id)

        # Get or create pending order (cart)
        order, created = Order.objects.get_or_create(
            user=request.user,
            status="Pending",
            defaults={"created_at": timezone.now()}
        )

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


# 🟢 View cart/order list - FIXED
@login_required
def order_list(request):
    # Get pending orders (cart) for the user
    orders = Order.objects.filter(user=request.user, status="Pending")

    # Keep items as a QuerySet, don't convert to list
    items = OrderItem.objects.filter(order__in=orders) if orders.exists() else OrderItem.objects.none()

    total_quantity = sum(item.quantity for item in items)

    context = {
        "items": items,
        "total_quantity": total_quantity,
        "has_items": items.exists()  # Now this works because items is a QuerySet
    }
    return render(request, "order_list.html", context)


# 🟢 Admin: Manage delivery
@login_required
def delivery_page(request):
    # Check if user is staff/admin
    if not request.user.is_staff:
        messages.error(request, "⚠️ Access denied. Admin privileges required.")
        return redirect('admin_menu')

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        action = request.POST.get("action")

        try:
            order = Order.objects.get(id=order_id)

            # Process order status changes
            if action == "process":
                order.status = "Processing"
                order.save()
                messages.success(request, f"🔄 Order #{order.id} is now being processed.")

            elif action == "ship":
                # Check stock availability for all items
                can_ship = True
                insufficient_stock_items = []

                for item in order.items.all():
                    if item.medicine.stock_quantity < item.quantity:
                        can_ship = False
                        insufficient_stock_items.append(
                            f"{item.medicine.name} (Available: {item.medicine.stock_quantity}, Needed: {item.quantity})"
                        )

                if not can_ship:
                    messages.error(
                        request,
                        f"⚠️ Cannot ship Order #{order.id}. Insufficient stock for: " +
                        "; ".join(insufficient_stock_items)
                    )
                else:
                    # Deduct stock using transaction to ensure data consistency
                    with transaction.atomic():
                        for item in order.items.all():
                            medicine = item.medicine
                            medicine.stock_quantity -= item.quantity
                            medicine.save()

                    order.status = "Shipped"
                    order.save()
                    messages.success(request, f"🚚 Order #{order.id} marked as Out for Delivery!")

            elif action == "complete":
                order.status = "Completed"
                order.save()
                messages.success(request, f"✅ Order #{order.id} marked as completed!")

            elif action == "cancel":
                order.status = "Cancelled"
                order.save()
                messages.warning(request, f"❌ Order #{order.id} cancelled.")

            elif action == "reopen":
                order.status = "Pending"
                order.save()
                messages.info(request, f"🔄 Order #{order.id} reopened.")

        except Order.DoesNotExist:
            messages.error(request, "⚠️ Order not found.")
        except Exception as e:
            messages.error(request, f"⚠️ Error processing order: {str(e)}")

        return redirect("delivery_page")

    # Show orders that are in active delivery states (excluding Completed and Cancelled)
    orders = Order.objects.exclude(
        status__in=["Completed", "Cancelled"]
    ).select_related('user').prefetch_related('items__medicine').order_by("-created_at")

    return render(request, "delivery_page.html", {"orders": orders})


# 🟢 Remove item from order
@login_required
def remove_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    medicine_name = item.medicine.name
    item.delete()

    # Check if order has no more items and delete empty order
    if item.order.items.count() == 0:
        item.order.delete()

    messages.success(request, f"🗑️ {medicine_name} removed from your order.")
    return redirect("order_list")


# 🟢 Update item quantity
@login_required
def update_order_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
        quantity = int(request.POST.get("quantity", 1))

        if quantity <= 0:
            item.delete()
            messages.success(request, f"🗑️ {item.medicine.name} removed from your order.")
        elif quantity > item.medicine.stock_quantity:
            messages.warning(request, f"⚠️ Only {item.medicine.stock_quantity} available in stock.")
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, f"📝 {item.medicine.name} quantity updated to {quantity}.")

    return redirect("order_list")


# 🟢 Checkout
@login_required
def order_checkout(request):
    try:
        # Get the user's pending order (cart)
        order = Order.objects.get(user=request.user, status="Pending")

        # Check stock availability before checkout
        can_checkout = True
        for item in order.items.all():
            if item.quantity > item.medicine.stock_quantity:
                can_checkout = False
                messages.warning(
                    request,
                    f"⚠️ Not enough stock for {item.medicine.name}. "
                    f"Available: {item.medicine.stock_quantity}, In cart: {item.quantity}"
                )

        if not can_checkout:
            return redirect("order_list")

        # Change status from Pending (cart) to Processing (checked out)
        order.status = "Processing"
        order.save()
        messages.success(request, "✅ Your order has been placed successfully! It's now awaiting confirmation.")

    except Order.DoesNotExist:
        messages.warning(request, "⚠️ No items in your cart.")

    return redirect("order_list")


# 🟢 Track delivery
@login_required
def track_delivery(request):
    orders = Order.objects.filter(user=request.user).exclude(status="Pending").order_by("-created_at")
    return render(request, "track_delivery.html", {"orders": orders})


# 🟢 Order history
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).exclude(status="Pending").order_by("-created_at")
    return render(request, "order_history.html", {"orders": orders})


# 🟢 Order details
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})