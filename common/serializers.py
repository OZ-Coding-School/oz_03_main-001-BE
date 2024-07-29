from rest_framework import serializers

from .models import Allergy


class AllergySerializer(serializers.ModelSerializer[Allergy]):
    class Meta:
        model = Allergy
        fields = "__all__"
