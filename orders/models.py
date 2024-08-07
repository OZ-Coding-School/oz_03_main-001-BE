from django.db import models

from common.models import CommonModel
from users.models import User


class Order(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    detail_address = models.TextField(blank=True)
    cooking_memo = models.TextField(blank=True)
    delivery_memo = models.TextField(blank=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    is_disposable = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(default=0)

    COMPLETED = 1
    CANCELLED = -1

    STATUS_CHOICES = (
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=COMPLETED)


class OrderItem(CommonModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    lunch = models.ForeignKey("lunch.Lunch", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["order", "lunch"], name="unique_order_lunch")]

    def __str__(self) -> str:
        return f"{self.quantity} x {self.lunch.name} in Order {self.order.id}"
