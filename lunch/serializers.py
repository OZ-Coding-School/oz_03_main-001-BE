from django.db import transaction
from rest_framework import serializers

from menus.models import Menu
from menus.serializers import MenuSerializer

from .models import Lunch, LunchMenu


class LunchMenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField(read_only=True)
    kcal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LunchMenu
        fields = ["id", "quantity", "name", "kcal"]

    def get_name(self, obj):
        return obj.menu.name

    def get_kcal(self, obj):
        return obj.menu.kcal


class LunchMenuDetailSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()

    class Meta:
        model = LunchMenu
        fields = ["quantity", "menu"]


class LunchSerializer(serializers.ModelSerializer[Lunch]):
    menus = LunchMenuSerializer(many=True, write_only=True)
    lunch_menu = LunchMenuDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Lunch
        fields = ["name", "description", "total_price", "total_kcal", "image_url", "menus", "lunch_menu"]

    @transaction.atomic
    def create(self, validated_data):
        menus_data = validated_data.pop("menus")
        lunch = Lunch.objects.create(**validated_data)

        for menu_data in menus_data:
            menu = Menu.objects.get(id=menu_data["id"])

            LunchMenu.objects.create(menu=menu, lunch=lunch, quantity=menu_data["quantity"])

            lunch.update_total_price()
            lunch.update_total_kcal()

        return lunch

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.image_url = validated_data.get("image_url", instance.image_url)
        instance.save()

        return instance
