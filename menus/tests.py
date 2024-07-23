from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menus.models import Menu, MenuDetailCategory
from common.models import Allergy
from .serializers import MenuDetailCategorySerializer, MenuWithDetailSerializer
from common.serializers import AllergySerializer


class MenuAPITestCase(APITestCase):
    def setUp(self) -> None:
        for i in range(5):
            self.menu = Menu.objects.create(
                name="menu name",
                description="descriptionnnsss",
                kcal=333,
                image_url="https://naver.com",
                price=1000,
                category="bob",
            )

    def test_menu_list_get(self) -> None:
        url = reverse("menu-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), Menu.objects.count())

    def test_menu_detail_get(self) -> None:
        url = reverse("menu-detail", kwargs={"pk": self.menu.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], "menu name")

    def test_create_menu(self):
        url = reverse("menu-list")
        data = {
            "name": "테스트 메뉴",
            "description": "테스트 메뉴 설명",
            "kcal": 500,
            "image_url": "http://example.com/test.jpg",
            "price": 10000,
            "category": "chan",
            "menu_details": [
                {
                    "allergy": "메밀",
                    "detail_category": "상세 카테고리1"
                },
                {
                    "allergy": None,
                    "detail_category": "상세 카테고리2"
                }
            ]
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 6)
        self.assertEqual(MenuDetailCategory.objects.count(), 2)

        menu = Menu.objects.last()
        self.assertEqual(menu.name, "테스트 메뉴")
        self.assertEqual(menu.category, Menu.Category.CHAN.value)

        allergies = Allergy.objects.all()
        self.assertEqual(allergies.count(), 21)
        # self.assertEqual(allergies.first(), "메밀")

        print(allergies)
        print(allergies.first())

        print(MenuWithDetailSerializer(Menu.objects.all().last()).data)

        for item in MenuDetailCategory.objects.all():
            print(MenuDetailCategorySerializer(item).data)

        menu_details = MenuDetailCategory.objects.filter(menu=menu)
        self.assertEqual(menu_details.count(), 2)
        self.assertEqual(menu_details.first().allergy, "메밀")
        self.assertIsNone(menu_details.last().allergy)

        print(response.data)