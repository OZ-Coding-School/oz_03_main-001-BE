from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from common.models import Allergy


class UserTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.user_info_url = reverse("user_info")
        self.user_update_url = lambda pk: reverse("user", kwargs={"pk": pk})
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
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue("access_token" in response.cookies)
        self.assertTrue("refresh_token" in response.cookies)

    def test_login(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_info(self):
        response = self.client.get(self.user_info_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.count())

    def test_user_update(self):
        data = {"username": "updateduser", "email": "updateduser@example.com", "password": "!rldnd12"}
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put(self.user_update_url(self.test_user.pk), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updateduser")
        self.assertEqual(response.data["email"], "updateduser@example.com")

    def test_user_delete(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.delete(self.user_update_url(self.test_user.pk), format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.test_user.pk).exists())

    def test_logout(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_allergies(self):
    #     # Create some allergies
    #     allergy1 = Allergy.objects.create(name="메밀")
    #     allergy2 = Allergy.objects.create(name="밀")
    #     self.test_user.allergies.set([allergy1, allergy2])
    #     self.client.force_authenticate(user=self.test_user)
    #     response = self.client.get(self.allergies_url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["allergies"], {"메밀": True, "밀": True})

    def test_get_allergies(self):
        # Create some allergies
        allergy1 = Allergy.objects.create(name="메밀")
        allergy2 = Allergy.objects.create(name="밀")
        self.test_user.allergies.set([allergy1, allergy2])
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.allergies_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["allergies"], {"메밀": True, "밀": True})

    # def test_post_allergies(self):
    #     # Create some allergies
    #     Allergy.objects.create(name="메밀")
    #     Allergy.objects.create(name="밀")
    #     data = {"allergies": {"메밀": True, "밀": True}}
    #     self.client.force_authenticate(user=self.test_user)
    #     response = self.client.post(self.allergies_url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(set(self.test_user.allergies.values_list("name", flat=True)), {"메밀", "밀"})

    def test_post_allergies(self):
        # Create some allergies
        Allergy.objects.get_or_create(name="메밀")
        Allergy.objects.get_or_create(name="밀")
        data = {"allergies": {"메밀": True, "밀": True}}
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.allergies_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(self.test_user.allergies.values_list("name", flat=True)), {"메밀", "밀"})
