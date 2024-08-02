from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import Allergy
from users.models import User


class UserTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.user_info_url = reverse("user")
        self.user_update_url = reverse("user")
        self.logout_url = reverse("logout")
        self.allergies_url = reverse("allergies")

        # Create a test user
        self.test_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        refresh = RefreshToken.for_user(self.test_user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        Allergy.objects.all().delete()

    def test_signup(self):
        data = {"username": "newuser", "email": "newuser@example.com", "password": "!rldnd12"}
        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("access_token" in response.cookies)
        self.assertTrue("refresh_token" in response.cookies)

    def test_same_username(self):
        response = self.client.post(
            self.signup_url,
            {"username": "testuser", "email": "test123@example.com", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            "이미 사용 중인 아이디입니다. 다른 아이디를 사용해주세요.", response.json().get("error_message")
        )

    def test_same_email(self):
        response = self.client.post(
            self.signup_url,
            {"username": "giung", "email": "test@example.com", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            "이미 사용 중인 이메일입니다. 다른 이메일을 사용해주세요.", response.json().get("error_message")
        )

    def test_similar_password(self):
        response = self.client.post(
            self.signup_url, {"username": "giung", "email": "test123@example.com", "password": "!giung"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual("비밀번호가 비슷합니다. 다른 비밀번호를 사용해주세요.", response.json().get("error_message"))

    def test_login(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access_token" in response.data, f"응답 데이터: {response.data}")
        self.assertTrue("refresh_token" in response.data, f"응답 데이터: {response.data}")

    def test_user_info(self):
        response = self.client.get(self.user_info_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.test_user.username)
        self.assertEqual(response.data["email"], self.test_user.email)

    def test_user_update(self):
        data = {"username": "updateduser", "email": "updateduser@example.com", "password": "!rldnd12"}
        response = self.client.put(self.user_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updateduser")
        self.assertEqual(response.data["email"], "updateduser@example.com")

    def test_user_delete(self):
        response = self.client.delete(self.user_update_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.test_user.pk).exists())

    def test_logout(self):
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_allergies(self):
        allergy1 = Allergy.objects.create(name="메밀")
        allergy2 = Allergy.objects.create(name="밀")
        self.test_user.allergies.set([allergy1, allergy2])
        response = self.client.get(self.allergies_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        allergies_data = response.data.get("allergies", {})

        response_keys = set(allergies_data.keys())
        expected_keys = {"메밀", "밀"}

        self.assertEqual(response_keys, expected_keys)
        self.assertTrue(allergies_data.get("메밀"))
        self.assertTrue(allergies_data.get("밀"))

    def test_post_allergies(self):
        # Create some allergies
        Allergy.objects.get_or_create(name="대두")
        Allergy.objects.get_or_create(name="호두")
        data = {"allergies": {"대두": True, "호두": True}}
        response = self.client.post(self.allergies_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(self.test_user.allergies.values_list("name", flat=True)), {"대두", "호두"})
