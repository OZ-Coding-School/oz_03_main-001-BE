import os

import jwt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from typing_extensions import Any

from common.models import Allergy
from users.models import User

from .serializers import UserInfoSerializer, UserSerializer, UserUpdateSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponseRedirect | Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)  # type: ignore
            refresh_token = str(refresh)

            response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": serializer.data,
            }

            response = Response(response_data, status=status.HTTP_201_CREATED)
            response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Lax")
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Lax")
            return response

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request: Request) -> Response:
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        print(serializer.errors)
        return Response(serializer.errors, status=400)

    def delete(self, request: Request) -> Response:
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError("username and password are required")

        user = authenticate(username=username, password=password)
        assert user is not None
        print(user)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)  # type: ignore
        refresh_token = str(refresh)

        if user:
            login(request, user)
            return Response({"access_token": access, "refresh_token": refresh_token})

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        print("header : ", request.headers)
        logout(request)

        return Response(status=status.HTTP_200_OK)


class AllegiesView(APIView):
    permission_classes = [IsAuthenticated]

    # permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        if not hasattr(user, "allergies"):
            return Response({"error": "User allergies information not available"}, status=status.HTTP_400_BAD_REQUEST)

        user_allergies = user.allergies.all()
        allergies_dict = {allergy.name: True for allergy in user_allergies}

        return Response({"allergies": allergies_dict})

    def post(self, request: Request) -> Response:
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        if not hasattr(user, "allergies"):
            return Response({"error": "User allergies information not available"}, status=status.HTTP_400_BAD_REQUEST)

        allergies_data = request.data.get("allergies", {})

        if not isinstance(allergies_data, dict):
            raise ValidationError("Allergies should be a list of names.")

        allergy_names = [name for name, is_active in allergies_data.items() if is_active]

        allergies = Allergy.objects.filter(name__in=allergy_names)

        user.allergies.set(allergies)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user

        return Response({"id": user.id, "username": user.username})
