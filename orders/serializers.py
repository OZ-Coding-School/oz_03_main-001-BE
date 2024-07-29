from django.db import transaction
from rest_framework import serializers

from lunch.models import Lunch, LunchMenu
from lunch.serializers import LunchMenuSerializer
from orders.models import Order, OrderItem


class OrderLunchSerializer(serializers.ModelSerializer):
    menus = LunchMenuSerializer(many=True, write_only=True)
    lunch_menu = LunchMenuSerializer(many=True, read_only=True)

    class Meta:
        model = Lunch
        fields = ["id", "name", "description", "total_price", "menus", "lunch_menu"]


class OrderItemSerializer(serializers.ModelSerializer):
    lunch = OrderLunchSerializer()

    class Meta:
        model = OrderItem
        fields = ["lunch", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "user",
            "request_things",
            "name",
            "status",
            "address",
            "contact_number",
            "is_disposable",
            "total_price",
            "items",
            "created_at",
        ]

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            lunch_data = item_data.pop("lunch")
            menus_data = lunch_data.pop("menus")

            lunch = Lunch.objects.create(**lunch_data)

            for menu_data in menus_data:
                lm = LunchMenu.objects.create(
                    lunch_id=lunch.pk,
                    menu_id=menu_data["id"],
                    quantity=menu_data["quantity"],
                )

                lm.kcal = lm.menu.kcal * lm.quantity
                lm.save()

            OrderItem.objects.create(order=order, lunch=lunch, **item_data)

        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()

        return instance
