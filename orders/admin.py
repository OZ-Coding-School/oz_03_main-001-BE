from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):  # type: ignore
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):  # type: ignore
    pass
