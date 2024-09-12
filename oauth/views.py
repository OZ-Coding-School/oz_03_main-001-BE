import os
from typing import Dict, Optional

import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


@require_http_methods(["GET"])
def kakao_login(request: HttpRequest) -> HttpResponse:
    login_url = os.environ.get("KAKAO_LOGIN_URL")
    client_id = os.environ.get("KAKAO_CLIENT_ID")
    redirect_uri = os.environ.get("KAKAO_REDIRECT_URI")

    kakao_auth_url = f"{login_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

    return redirect(kakao_auth_url)


@require_http_methods(["GET"])
def kakao_callback(request: HttpRequest) -> HttpResponse:
    code = request.GET.get("code")

    token_data: Dict[str, Optional[str]] = {
        "grant_type": "authorization_code",
        "client_id": os.environ.get("KAKAO_CLIENT_ID"),
        "redirect_uri": os.environ.get("KAKAO_REDIRECT_URI"),
        "code": code,
        "client_secret": os.environ.get("KAKAO_CLIENT_SECRET"),
    }

    token_headers: Dict[str, str] = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    kakao_token_url = os.environ.get("KAKAO_TOKEN_URL")

    if kakao_token_url is None:
        raise ValueError("KAKAO_TOKEN_URL 환경 변수가 설정되어 있지 않습니다")

    token_response = requests.post(kakao_token_url, headers=token_headers, data=token_data, timeout=30)

    if token_response.status_code != 200:
        response_content = token_response.content.decode("utf-8")

        return HttpResponse(
            f"카카오 토큰 받기 실패 💀 {response_content}",
            status=500,
        )

    access_token = token_response.json()["access_token"]

    kakao_profile_url = os.environ.get("KAKAO_PROFILE_URL")

    if kakao_profile_url is None:
        raise ValueError("KAKAO_PROFILE_URL 환경 변수가 설정되어 있지 않습니다")

    profile_response = requests.get(
        kakao_profile_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        },
        timeout=30,
    )

    profile_info = profile_response.json()

    kakao_email = profile_info.get("kakao_account", {}).get("email")
    kakao_username = profile_info.get("properties", {}).get("nickname")

    user, created = User.objects.get_or_create(
        email=kakao_email,
        defaults={
            "username": kakao_username,
        },
    )

    if created:
        response = redirect("https://dosirock.store/all")
        user.set_unusable_password()
        user.save()
    else:
        response = redirect("https://dosirock.store")

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)  # type: ignore
    refresh_token = str(refresh)

    response.set_cookie(
        "access_token",
        access_token,
        httponly=False,
        secure=True,
        samesite="Lax",
        domain=".dosirock.store",
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=False,
        secure=True,
        samesite="Lax",
        domain=".dosirock.store",
    )

    return response


@require_http_methods(["GET"])
def kakao_logout(request: HttpRequest) -> HttpResponse:
    client_id = os.environ.get("KAKAO_CLIENT_ID")
    redirect_logout_url = os.environ.get("KAKAO_REDIRECT_KAKAO_LOGOUT_URI")
    logout_url = os.environ.get("KAKAO_LOGOUT_URL")

    if not client_id or not redirect_logout_url or not logout_url:
        return HttpResponse(
            f"Missing environment variables. Client ID: {client_id}, Redirect URL: {redirect_logout_url}, Logout URL: {logout_url}",
            status=500,
        )

    kakao_logout_url = f"{logout_url}?client_id={client_id}&logout_redirect_uri={redirect_logout_url}"

    return redirect(kakao_logout_url)
