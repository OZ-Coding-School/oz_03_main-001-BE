from django.db import transaction
from rest_framework import serializers

from lunch.models import Lunch, LunchMenu
from lunch.serializers import LunchMenuSerializer
from orders.models import Order, OrderItem


class OrderLunchSerializer(serializers.ModelSerializer):
    menus = LunchMenuSerializer(many=True)

    class Meta:
        model = Lunch
        fields = ["id", "name", "description", "menus", "total_kcal"]


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
                LunchMenu.objects.create(lunch=lunch, menu_id=menu_data["id"], quantity=menu_data["quantity"])

            OrderItem.objects.create(order=order, lunch=lunch, **item_data)

        return order


class OrderDetailSerializer(serializers.ModelSerializer):
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
        ]
