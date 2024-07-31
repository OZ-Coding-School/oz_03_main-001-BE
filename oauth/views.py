import json
import os

import requests
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


@require_http_methods(["GET"])
def kakao_login(request):
    login_url = os.environ.get("KAKAO_LOGIN_URL")
    client_id = os.environ.get("KAKAO_CLIENT_ID")
    redirect_uri = os.environ.get("KAKAO_REDIRECT_URI")

    kakao_auth_url = f"{login_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

    return redirect(kakao_auth_url)


@require_http_methods(["GET"])
def kakao_callback(request):
    code = request.GET.get("code")
    token_data = {
        "grant_type": "authorization_code",
        "client_id": os.environ.get("KAKAO_CLIENT_ID"),
        "redirect_uri": os.environ.get("KAKAO_REDIRECT_URI"),
        "code": code,
        "client_secret": os.environ.get("KAKAO_CLIENT_SECRET"),
    }

    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    token_response = requests.post(
        os.environ.get("KAKAO_TOKEN_URL"), headers=token_headers, data=token_data, timeout=30
    )

    if token_response.status_code != 200:
        return HttpResponse(
            f"카카오 토큰 받기 실패 💀 {token_response.content}",
            status=500,
        )

    access_token = token_response.json()["access_token"]

    profile_response = requests.get(
        os.environ.get("KAKAO_PROFILE_URL"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        },
        timeout=30,
    )

    profile_info = profile_response.json()

    print(json.dumps(profile_info))

    # Retrieve or create the user
    kakao_id = profile_info["id"]
    kakao_email = profile_info.get("kakao_account", {}).get("email")
    kakao_username = profile_info.get("properties", {}).get("nickname")

    user, created = User.objects.get_or_create(
        email=kakao_email,
        defaults={
            "username": kakao_username,
            # "password": User.objects.make_random_password(),
        },
    )

    if created:

        user.set_unusable_password()
        # 비밀번호를 사용한 로그인을 안되게 한다.
        user.save()

    print(user)

    # Generate tokens using SimpleJWT
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    print(f"access_token: {access_token}\nrefresh_token: {refresh_token}")

    # response = JsonResponse(profile_info, status=200)
    response = redirect(reverse("/"))
    response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Lax")
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Lax")

    return response


@require_http_methods(["GET"])
def kakao_logout(request):
    client_id = os.environ.get("KAKAO_CLIENT_ID")
    redirect_logout_url = os.environ.get("KAKAO_REDIRECT_KAKAO_LOGOUT_URL_URI")
    logout_url = os.environ.get("KAKAO_LOGOUT_URL")

    if not client_id or not redirect_logout_url or not logout_url:
        return HttpResponse(
            f"Missing environment variables. Client ID: {client_id}, Redirect URL: {redirect_logout_url}, Logout URL: {logout_url}",
            status=500,
        )

    kakao_logout_url = f"{logout_url}?client_id={client_id}&logout_redirect_uri={redirect_logout_url}"

    return redirect(kakao_logout_url)
