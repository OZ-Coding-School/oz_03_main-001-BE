from rest_framework import serializers

from .models import Lunch, LunchMenu


class LunchMenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LunchMenu
        fields = ["id", "quantity", "kcal", "name"]

    def get_name(self, obj):
        return obj.menu.name


class LunchSerializer(serializers.ModelSerializer[Lunch]):
    menus = LunchMenuSerializer(many=True, read_only=True)

    class Meta:
        model = Lunch
        fields = ["name", "description", "total_price", "image_url", "menus"]
