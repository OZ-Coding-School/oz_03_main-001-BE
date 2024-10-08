from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import Allergy
from lunch.models import Lunch, LunchMenu
from menus.serializers import MenuWithDetailSerializer
from users.models import User
from utils.test_helper import create_menu


class LunchAPITestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword", status=2
        )

        refresh = RefreshToken.for_user(self.test_user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        allergy_names = ["밀", "돼지고기"]
        allergies = Allergy.objects.filter(name__in=allergy_names)

        self.test_user.allergies.set(allergies)

        menu1 = create_menu(name="test_menu1")
        menu2 = create_menu(name="test_menu2")

        menu_data = {
            "name": "돼지고기 김치 볶음",
            "description": "descriptionnnsss",
            "kcal": 333,
            "image_url": "https://naver.com",
            "price": 1000,
            "category": "chan",
            "menu_details": [
                {"allergy": "대두", "detail_category": "볶음"},
                {"allergy": "돼지고기", "detail_category": "돼지고기"},
            ],
        }
        menu_data3 = {
            "name": "소고기 김치 볶음",
            "description": "descriptionnnsss",
            "kcal": 600,
            "image_url": "https://naver.com",
            "price": 1000,
            "category": "chan",
            "menu_details": [
                {"allergy": "대두", "detail_category": "볶음"},
                {"allergy": "돼지고기", "detail_category": "돼지고기"},
            ],
        }
        menu_data4 = {
            "name": "고등어 김치 볶음",
            "description": "descriptionnnsss",
            "kcal": 400,
            "image_url": "https://naver.com",
            "price": 1000,
            "category": "chan",
            "menu_details": [
                {"allergy": "대두", "detail_category": "볶음"},
                {"allergy": "돼지고기", "detail_category": "돼지고기"},
            ],
        }

        menu_data2 = {
            "name": "된장찌개",
            "description": "descriptionnnsss",
            "kcal": 500,
            "image_url": "https://naver.com",
            "price": 1000,
            "category": "guk",
            "menu_details": [
                {"allergy": "대두", "detail_category": "볶음"},
            ],
        }

        menu_data5 = {
            "name": "김치찌개",
            "description": "descriptionnnsss",
            "kcal": 676,
            "image_url": "https://naver.com",
            "price": 1000,
            "category": "guk",
            "menu_details": [
                {"allergy": "대두", "detail_category": "볶음"},
            ],
        }

        serializer = MenuWithDetailSerializer(data=menu_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = MenuWithDetailSerializer(data=menu_data2)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = MenuWithDetailSerializer(data=menu_data3)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = MenuWithDetailSerializer(data=menu_data4)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = MenuWithDetailSerializer(data=menu_data5)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        for i in range(1, 11):
            lunch = Lunch.objects.create(
                store=self.test_user,
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

    def test_random_lunch_get(self):
        url = reverse("lunch-random")

        with self.assertNumQueries(4):
            res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_random_lunch_with_allergy_get(self):
        base_url = reverse("lunch-random")
        url = f"{base_url}?allergy=true"

        with self.assertNumQueries(4):
            res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
