from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import Allergy
from menus.models import Menu, MenuDetailCategory
from menus.serializers import MenuWithDetailSerializer
from users.models import User
from utils.test_helper import create_menu


class MenuAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword", status=2
        )
        refresh = RefreshToken.for_user(self.test_user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.menu = create_menu(name="test_menu1")
        create_menu(name="test_menu2")
        create_menu(name="test_menu3")
        create_menu(name="test_menu4")

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

        menu_data2 = {
            "name": "된장찌개",
            "description": "descriptionnnsss",
            "kcal": 333,
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
                    "allergy": "복숭아",
                    "detail_category": "Updated Detail Category",
                }
            ],
        }

    def test_get_allergies_search_menu(self) -> None:
        base_url = reverse("menu-list")
        url = f"{base_url}?category=guk&allergy=조개류&search=찌개"

        with self.assertNumQueries(4):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], "된장찌개")

    def test_get_search_menu(self) -> None:
        base_url = reverse("menu-list")
        url = f"{base_url}?category=chan&search=돼지"

        with self.assertNumQueries(4):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], "돼지고기 김치 볶음")

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
        self.assertEqual(len(res.data), 4)
        self.assertEqual(res.data["current_page"], 1)

    def test_menu_detail_get(self) -> None:
        url = reverse("menu-detail", kwargs={"pk": self.menu.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], "test_menu1")

    def test_create_menus(self) -> None:
        url = reverse("menu-list")
        datas = []
        data1 = {
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

        data2 = {
            "name": "테스트 메뉴2",
            "description": "테스트 메뉴 설명",
            "kcal": 4500,
            "image_url": "http://example.com/test.jpg",
            "price": 50000,
            "category": "bob",
            "menu_details": [
                {"allergy": "돼지고기", "detail_category": "상세 카테고리1"},
            ],
        }

        datas.append(data1)
        datas.append(data2)

        response = self.client.post(url, data=datas, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]["name"], "테스트 메뉴")

    def test_create_menu(self) -> None:
        url = reverse("menu-list")
        data = [
            {
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
        ]

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 7)
        self.assertEqual(MenuDetailCategory.objects.count(), 13)

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
