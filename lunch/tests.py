from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lunch.models import Lunch, LunchMenu
from menus.models import Menu
from utils.test_helper import create_menu


class LunchAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="test@naver.com", password="1234")
        self.client.login(username="testuser", password="1234")

        menu1 = create_menu(name="test_menu1")
        menu2 = create_menu(name="test_menu2")

        for i in range(1, 11):
            lunch = Lunch.objects.create(
                store=user,
                name=f"test Lunch{i}",
                description="test lunch set",
                image_url="http://example.com/image.jpg",
            )

            LunchMenu.objects.create(lunch=lunch, menu=menu1, quantity=2, kcal=500)
            LunchMenu.objects.create(lunch=lunch, menu=menu2, quantity=1, kcal=300)

            lunch.update_total_kcal()
            lunch.update_total_price()

    def test_lunch_get(self):
        url = reverse("lunch-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
        self.assertEqual(len(res.data["results"]), 10)

    def test_lunch_post(self):
        lunch_data = {
            "name": "도시락1",
            "description": "신선한 도시락",
            "menus": [
                {
                    "id": 1,
                    "quantity": 1,
                },
                {
                    "id": 2,
                    "quantity": 2,
                },
            ],
        }

        url = reverse("lunch-list")
        res = self.client.post(url, lunch_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], lunch_data["name"])
        self.assertEqual(res.data["description"], lunch_data["description"])
        self.assertEqual(res.data["total_kcal"], 999)
        self.assertEqual(res.data["total_price"], 3000)

    def test_lunch_put(self):
        lunch_data = {
            "name": "내가 만든 도시락",
            "description": "맛있는 도시락",
            "menus": [
                {
                    "id": 1,
                    "quantity": 1,
                },
                {
                    "id": 2,
                    "quantity": 2,
                },
            ],
        }
        url = reverse("lunch-detail", kwargs={"pk": 1})
        res = self.client.put(url, lunch_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], lunch_data["name"])

    def test_lunch_delete(self):
        url = reverse("lunch-detail", kwargs={"pk": 1})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Lunch.DoesNotExist):
            Lunch.objects.get(pk=1)
