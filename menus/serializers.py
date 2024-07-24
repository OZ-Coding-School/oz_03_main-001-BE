from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from common.models import Allergy
from common.serializers import AllergySerializer

from .models import Menu, MenuDetailCategory


class MenuDetailCategorySerializer(serializers.ModelSerializer[MenuDetailCategory]):
    allergy = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    allergy_info = AllergySerializer(source="allergy", read_only=True)
    menu: Menu = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = MenuDetailCategory
        fields = ["id", "allergy", "allergy_info", "detail_category", "menu"]

    def create(self, validated_data) -> MenuDetailCategory:
        allergy_name = validated_data.pop("allergy", None)
        instance = MenuDetailCategory.objects.create(**validated_data)
        if allergy_name:
            allergy = get_object_or_404(Allergy, name=allergy_name)
            instance.allergy = allergy
            instance.save()
        return instance


class MenuWithDetailSerializer(serializers.ModelSerializer[Menu]):
    menu_details = MenuDetailCategorySerializer(many=True)

    class Meta:
        model = Menu
        fields = ["id", "name", "description", "kcal", "image_url", "price", "category", "menu_details"]

    @transaction.atomic
    def create(self, validated_data) -> Menu:
        menu_details_data = validated_data.pop("menu_details")
        menu = Menu.objects.create(**validated_data)

        for menu_detail_data in menu_details_data:
            serializer = MenuDetailCategorySerializer(data=menu_detail_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(menu=menu)
        return menu

    @transaction.atomic
    def update(self, instance, validated_data):
        menu_details_data = validated_data.pop("menu_details", [])
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.kcal = validated_data.get("kcal", instance.kcal)
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
