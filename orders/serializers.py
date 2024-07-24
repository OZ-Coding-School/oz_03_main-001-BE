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

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])
        instance.request_things = validated_data.get("request_things", instance.request_things)
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.image_url = validated_data.get("image_url", instance.image_url)
        instance.price = validated_data.get("price", instance.price)
        instance.category = validated_data.get("category", instance.category)
        instance.save()

        for detail_data in menu_details_data:
            detail_id = detail_data.get("id")

            if detail_id:
                detail_instance = MenuDetailCategory.objects.get(id=detail_id, menu=instance)
                allergy = get_object_or_404(Allergy, name=detail_data.get("allergy"))
                detail_instance.allergy = detail_data.get(allergy, detail_instance.allergy)
                detail_instance.detail_category = detail_data.get("detail_category", detail_instance.detail_category)
                detail_instance.save()
            else:
                MenuDetailCategory.objects.create(menu=instance, **detail_data)

        return instance
