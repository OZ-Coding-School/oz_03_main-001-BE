from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menus.models import Menu


class MenuAPITestCase(APITestCase):
    def setUp(self) -> None:
        for i in range(5):
            self.menu = Menu.objects.create(
                name="menu name",
                description="descriptionnnsss",
                kcal=333,
                image_url="https://naver.com",
                price=1000,
                category="bo",
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
