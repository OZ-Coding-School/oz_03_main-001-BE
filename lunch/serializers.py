from rest_framework import serializers

from menus.models import Menu

from .models import Lunch, LunchMenu


class LunchMenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = LunchMenu
        fields = ["id", "quantity", "kcal"]

    def validate_menu(self, value):
        if not Menu.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid menu ID")
        return value


class LunchSerializer(serializers.ModelSerializer[Lunch]):
    menus = LunchMenuSerializer(many=True, read_only=True)

    class Meta:
        model = Lunch
        fields = ["name", "description", "total_price", "image_url", "menus"]
