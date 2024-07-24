from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import Allergy
from menus.models import Menu, MenuDetailCategory
from utils.test_helper import create_menu


class MenuAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.menu = create_menu(name="test_menu1")

        self.valid_payload = {
            "name": "Updated Menu",
            "description": "Updated Description",
            "kcal": 200,
            "image_url": "http://example.com/new_image.jpg",
            "price": 2000,
            "category": "bob",
            "menu_details": [{"id": 1, "allergy": "복숭아", "detail_category": "Updated Detail Category"}],
        }

        self.invalid_payload = {
            "name": "",
            "description": "Updated Description",
            "kcal": 200,
            "image_url": "http://example.com/new_image.jpg",
            "price": 2000,
            "category": "bob",
            "menu_details": [
                {
                    "id": 1,
                    "allergy": "복숭아",
                    "detail_category": "Updated Detail Category",
                }
            ],
        }

    def test_update_valid_menu(self) -> None:
        url = reverse("menu-detail", kwargs={"pk": self.menu.pk})
        response = self.client.put(url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.name, self.valid_payload["name"])

    def test_update_invalid_menu(self) -> None:
        url = reverse("menu-detail", kwargs={"pk": self.menu.pk})
        response = self.client.put(url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_menu_list_get(self) -> None:
        url = reverse("menu-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), Menu.objects.count())

    def test_menu_detail_get(self) -> None:
        url = reverse("menu-detail", kwargs={"pk": self.menu.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], "test_menu1")

    def test_create_menu(self) -> None:
        url = reverse("menu-list")
        data = {
            "name": "테스트 메뉴",
            "description": "테스트 메뉴 설명",
            "kcal": 500,
            "image_url": "http://example.com/test.jpg",
            "price": 10000,
            "category": "chan",
            "menu_details": [
                {"allergy": "메밀", "detail_category": "상세 카테고리1"},
                {"allergy": None, "detail_category": "상세 카테고리2"},
            ],
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(MenuDetailCategory.objects.count(), 4)

        menu = Menu.objects.last()
        self.assertEqual(menu.name, "테스트 메뉴")
        self.assertEqual(menu.category, Menu.Category.CHAN.value)

        allergies = Allergy.objects.all()
        self.assertEqual(allergies.count(), 21)
        self.assertEqual(allergies.first().name, "메밀")

        menu_details = MenuDetailCategory.objects.filter(menu=menu)
        self.assertEqual(menu_details.count(), 2)
        self.assertEqual(menu_details.first().allergy.name, "메밀")
        self.assertIsNone(menu_details.last().allergy)

        print(response.data)
