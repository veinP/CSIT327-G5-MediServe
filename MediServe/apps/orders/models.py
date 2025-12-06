from django.db import models
from django.conf import settings
from apps.medicine.models import Medicine


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Out for Delivery"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    DRIVERS = [
        "Marco Dela Cruz",
        "Johnrey Santos",
        "Carlito Mendoza",
        "Jerome Villanueva",
        "Renzo Ramirez",
        "Gabriel Torres",
        "Alfred Navarro",
        "Kristoffer Soriano",
        "Ralph Gutierrez",
        "Leo Manalang",
    ]
    DRIVER_CHOICES = [(driver, driver) for driver in DRIVERS]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver = models.CharField(max_length=255, null=True, blank=True, choices=DRIVER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    queue_number = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "tblorders"
        ordering = ['queue_number', '-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.full_name} ({self.status})"

    # -----------------------------
    # QUEUE LOGIC
    # -----------------------------
    def assign_queue_number(self):
        pending_orders = Order.objects.filter(
            status__in=['Pending', 'Processing'],
            queue_number__isnull=False
        ).exclude(pk=self.pk).order_by('queue_number')

        is_priority = self.user.senior_citizen_id or self.user.pwd_id

        if is_priority:
            regular_orders = pending_orders.filter(
                user__senior_citizen_id__isnull=True,
                user__pwd_id__isnull=True
            )
            priority_orders = pending_orders.exclude(id__in=regular_orders)

            if priority_orders.exists():
                last_priority = priority_orders.last()
                insert_position = last_priority.queue_number + 1
            else:
                insert_position = 1

            self.queue_number = insert_position

            orders_to_shift = pending_orders.filter(queue_number__gte=insert_position)
            for order in orders_to_shift:
                order.queue_number += 1
                order.save()

        else:
            if pending_orders.exists():
                last_order = pending_orders.last()
                self.queue_number = last_order.queue_number + 1
            else:
                self.queue_number = 1

        self.save()

    def remove_from_queue(self):
        if not self.queue_number:
            return

        current_queue = self.queue_number

        orders_to_shift = Order.objects.filter(
            status__in=['Pending', 'Processing'],
            queue_number__gt=current_queue
        ).order_by('queue_number')

        for order in orders_to_shift:
            order.queue_number -= 1
            order.save()

        self.queue_number = None
        self.save()

    def get_queue_position(self):
        if self.status not in ['Pending', 'Processing']:
            return None

        active_orders = Order.objects.filter(
            status__in=['Pending', 'Processing']
        ).order_by('queue_number')

        for pos, order in enumerate(active_orders, start=1):
            if order.id == self.id:
                return pos
        return None

    def can_user_access(self, user):
        return self.user == user

    def is_priority_user(self):
        return bool(self.user.senior_citizen_id or self.user.pwd_id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_request = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tblorderitems"

    def __str__(self):
        return f"{self.medicine.name} × {self.quantity}"
