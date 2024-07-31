from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import Allergy
from users.models import User

# TODO 테스트 코드 다시 확인 및 다른 앱 테스트 코드 이어서 작성


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

        Allergy.objects.all().delete()

    def test_signup(self):
        data = {"username": "newuser", "email": "newuser@example.com", "password": "!rldnd12"}
        response = self.client.post(self.signup_url, data, format="json")

        # 리디렉션 발생 여부 확인
        if response.status_code == 302:
            print("Redirected to:", response["Location"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("access_token" in response.cookies)
        self.assertTrue("refresh_token" in response.cookies)

    def test_login(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access_token" in response.data, f"응답 데이터: {response.data}")
        self.assertTrue("refresh_token" in response.data, f"응답 데이터: {response.data}")

    def test_user_info(self):
        # Authenticate user
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.user_info_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.test_user.username)
        self.assertEqual(response.data["email"], self.test_user.email)

    def test_user_update(self):
        data = {"username": "updateduser", "email": "updateduser@example.com", "password": "!rldnd12"}
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put(self.user_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updateduser")
        self.assertEqual(response.data["email"], "updateduser@example.com")

    def test_user_delete(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.delete(self.user_update_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.test_user.pk).exists())

    def test_logout(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_allergies(self):
        # Create some allergies
        allergy1 = Allergy.objects.create(name="메밀")
        allergy2 = Allergy.objects.create(name="밀")
        self.test_user.allergies.set([allergy1, allergy2])
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.allergies_url, format="json")
        print("응답 데이터:", response.data)

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
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.allergies_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(self.test_user.allergies.values_list("name", flat=True)), {"대두", "호두"})
