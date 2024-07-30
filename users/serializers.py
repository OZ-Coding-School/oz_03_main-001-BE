from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import User
from common.models import Allergy
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user = User(**data)

        errors = dict()
        try:
            validate_password(password=data["password"], user=user)
        except ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)

    def create(self, validated_data):
        user = User(**validated_data)

        user.set_password(validated_data["password"])
        user.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    allergies = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "created_at", "updated_at", "allergies"]
        extra_kwargs = {"password": {"write_only": True}}

    def get_allergies(self, obj):
        return {allergy.name: True for allergy in obj.allergies.all()}
