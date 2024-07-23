from rest_framework import serializers
from django.shortcuts import get_object_or_404
from common.models import Allergy
from common.serializers import AllergySerializer

from .models import Menu, MenuDetailCategory

class MenuSerializer(serializers.ModelSerializer[Menu]):
    class Meta:
        model = Menu
        fields = "__all__"


class MenuDetailCategorySerializer(serializers.ModelSerializer[MenuDetailCategory]):
    allergy = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    allergy_info = AllergySerializer(source='allergy', read_only=True)

    class Meta:
        model = MenuDetailCategory
        fields = ['allergy', 'allergy_info', 'detail_category']

    def create(self, validated_data):
        allergy_name = validated_data.pop('allergy', None)
        instance = MenuDetailCategory.objects.create(**validated_data)
        if allergy_name:
            allergy = Allergy.objects.get(name=allergy_name)
            print(allergy)
            # allergy = get_object_or_404(Allergy, name=allergy_name)
            # print("zz, ", allergy)
            instance.allergy = allergy
            instance.save()
        return instance


class MenuWithDetailSerializer(serializers.ModelSerializer):
    menu_details = MenuDetailCategorySerializer(many=True)

    class Meta:
        model = Menu
        fields = ["name", "description", "kcal", "image_url", "price", "category", "menu_details"]

    def create(self, validated_data) -> Menu:
        print("hi", validated_data)
        menu_details_data = validated_data.pop("menu_details")
        print("hi2", menu_details_data)
        menu = Menu.objects.create(**validated_data)

        for menu_detail_data in menu_details_data:
            serializer = MenuDetailCategorySerializer(data=menu_detail_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(menu=menu)
        return menu

            #
            # allergy_label = menu_detail_data.pop("allergy", None)
            # print(allergy_label)
            # if allergy_label:
            #     allergy = get_object_or_404(Allergy, name=allergy_label)
            #     menu_detail_data["allergy"] = allergy
            #     print("Zzxzx", menu_detail_data)
            # else:
            #     menu_detail_data["allergy"] = None
            # MenuDetailCategory.objects.create(menu=menu, **menu_detail_data)
        # return menu
