from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, ParseError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer, UserInfoSerializer
from users.models import User

from common.models import Allergy


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = redirect(reverse("/"))
            response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Lax")
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Lax")
            return response

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = User.objects.all()

        serializer = UserInfoSerializer(user, many=True)
        return Response(serializer.data)


class UserUpdateView(APIView):
    # TODO 인가 코드쪽 구현
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        print(serializer.errors)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.contrib.auth import authenticate, login, logout


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError("username and password are required")

        user = authenticate(username=username, password=password)
        print(user)

        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("header : ", request.headers)
        logout(request)

        return Response(status=status.HTTP_200_OK)


class AllegiesView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        user_allergies = user.allergies.all()

        allergies_dict = {allergy.name: True for allergy in user_allergies}
        return Response({"allergies": allergies_dict})

    def post(self, request):
        user = request.user

        allergies_data = request.data.get("allergies", {})

        if not isinstance(allergies_data, dict):
            raise ValidationError("Allergies should be a list of names.")

        allergy_names = [name for name, is_active in allergies_data.items() if is_active]

        allergies = Allergy.objects.filter(name__in=allergy_names)

        user.allergies.set(allergies)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
