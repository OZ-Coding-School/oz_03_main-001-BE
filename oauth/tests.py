import json
import os
from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class KakaoAuthTests(TestCase):
    def setUp(self):
        load_dotenv()

        self.client = Client()
        self.kakao_login_url = reverse("kakao_login")
        self.kakao_callback_url = reverse("kakao_callback")
        self.kakao_logout_url = reverse("kakao_logout")

        # 환경 변수 설정
        self.kakao_login_url_env = os.getenv("KAKAO_LOGIN_URL")
        self.kakao_token_url_env = os.getenv("KAKAO_TOKEN_URL")
        self.kakao_profile_url_env = os.getenv("KAKAO_PROFILE_URL")
        self.kakao_client_id_env = os.getenv("KAKAO_CLIENT_ID")
        self.kakao_redirect_uri_env = os.getenv("KAKAO_REDIRECT_URI")
        self.kakao_client_secret_env = os.getenv("KAKAO_SECRET")
        self.kakao_logout_url_env = os.getenv("KAKAO_LOGOUT_URL")
        self.kakao_redirect_logout_uri_env = os.getenv("KAKAO_REDIRECT_KAKAO_LOGOUT_URI")

        # 환경 변수 모킹
        patch.dict(
            "os.environ",
            {
                "KAKAO_LOGIN_URL": self.kakao_login_url_env,
                "KAKAO_TOKEN_URL": self.kakao_token_url_env,
                "KAKAO_PROFILE_URL": self.kakao_profile_url_env,
                "KAKAO_CLIENT_ID": self.kakao_client_id_env,
                "KAKAO_REDIRECT_URI": self.kakao_redirect_uri_env,
                "KAKAO_CLIENT_SECRET": self.kakao_client_secret_env,
                "KAKAO_LOGOUT_URL": self.kakao_logout_url_env,
                "KAKAO_REDIRECT_KAKAO_LOGOUT_URL_URI": self.kakao_redirect_logout_uri_env,
            },
        ).start()

    @patch("requests.post")
    def test_kakao_callback_success(self, mock_post):
        # Mock token response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "test_access_token"}

        # Mock profile response
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "id": 12345,
                "kakao_account": {"email": "test@example.com"},
                "properties": {"nickname": "testuser"},
            }

            response = self.client.get(self.kakao_callback_url, {"code": "test_code"})

            self.assertEqual(response.status_code, 302)  # Redirect status
            # Check if access_token cookie is set
            self.assertIn("access_token", response.cookies)
            self.assertTrue(response.cookies["access_token"].value.startswith("eyJ"))

            # Check if refresh_token cookie is set
            self.assertIn("refresh_token", response.cookies)
            self.assertTrue(response.cookies["refresh_token"].value.startswith("eyJ"))

            # Check user creation
            user = User.objects.get(email="test@example.com")
            self.assertEqual(user.username, "testuser")

    @patch("requests.post")
    def test_kakao_callback_failure(self, mock_post):
        # Mock token response failure
        mock_post.return_value.status_code = 400
        mock_post.return_value.content = b"error"

        response = self.client.get(self.kakao_callback_url, {"code": "test_code"})

        self.assertEqual(response.status_code, 500)  # Internal Server Error

    def test_kakao_logout(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200

            response = self.client.get(self.kakao_logout_url)

            # Validate that the URL is correctly formed
            expected_url = f"{self.kakao_logout_url_env}?client_id={self.kakao_client_id_env}&logout_redirect_uri={self.kakao_redirect_logout_uri_env}"
            self.assertEqual(response.url, expected_url)
            self.assertEqual(response.status_code, 302)  # Redirect status
