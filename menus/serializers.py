from rest_framework import serializers

from .models import Menu


class MenuSerializer(serializers.ModelSerializer[Menu]):
    class Meta:
        model = Menu
        fields = "__all__"
