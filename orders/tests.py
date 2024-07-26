from pprint import pprint

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils.test_helper import create_menu

from .models import Order
from .serializers import OrderSerializer


class OrderTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@naver.com", "1234")
        self.client.login(email="test@naver.com", password="1234")

        create_menu(name="menu1")
        create_menu(name="menu2")
        create_menu(name="menu3")
        create_menu(name="menu4")

        self.order_data = {
            "user": self.user.pk,
            "total_price": 17000,
            "status": 1,
            "request_things": "특별 요청사항",
            "name": "김철수",
            "address": "서울시 강남구",
            "contact_number": "010-1234-5678",
            "is_disposable": False,
            "items": [
                {
                    "quantity": 1,
                    "lunch": {
                        "name": "도시락1",
                        "description": "신선한 도시락",
                        "total_kcal": 1000,
                        "total_price": 10000,
                        "menus": [
                            {
                                "id": 1,
                                "quantity": 1,
                                "kcal": 500,
                            },
                            {
                                "id": 2,
                                "quantity": 2,
                                "kcal": 600,
                            },
                        ],
                    },
                },
                {
                    "quantity": 2,
                    "lunch": {
                        "name": "도시락2",
                        "description": "신선한 도시락2",
                        "image_url": "http://example.com/image.jpg",
                        "total_kcal": 900,
                        "total_price": 7000,
                        "menus": [
                            {
                                "id": 3,
                                "quantity": 1,
                                "kcal": 444,
                            },
                            {
                                "id": 4,
                                "quantity": 1,
                                "kcal": 444,
                            },
                        ],
                    },
                },
            ],
        }
        for i in range(2):
            serializer = OrderSerializer(data=self.order_data)
            serializer.is_valid()
            self.order = serializer.save()

    def test_order_list_get(self):
        url = reverse("order-list")

        # 로거 인스턴스 생성
        with self.assertNumQueries(6):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data['results']), 5)

    def test_order_post(self):
        url = reverse("order-list")
        response = self.client.post(url, data=self.order_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["total_price"], 17000)
        self.assertEqual(response.data["is_disposable"], False)

    def test_order_detail_get(self):
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["items"][1]["lunch"]["id"], 10)

    def test_order_update(self):
        order_data = {
            "user": self.user.pk,
            "total_price": 17000,
            "status": -1,
            "request_things": "특별 요청사항",
            "name": "김철수",
            "address": "서울시 강남구",
            "contact_number": "010-1234-5678",
            "is_disposable": False,
            "items": [
                {
                    "quantity": 1,
                    "lunch": {
                        "name": "도시락1",
                        "description": "신선한 도시락",
                        "total_kcal": 1000,
                        "menus": [
                            {
                                "id": 1,
                                "quantity": 1,
                                "kcal": 500,
                            },
                            {
                                "id": 2,
                                "quantity": 2,
                                "kcal": 600,
                            },
                        ],
                    },
                },
                {
                    "quantity": 2,
                    "lunch": {
                        "name": "도시락2",
                        "description": "신선한 도시락2",
                        "image_url": "http://example.com/image.jpg",
                        "total_kcal": 900,
                        "menus": [
                            {
                                "id": 3,
                                "quantity": 1,
                                "kcal": 444,
                            },
                            {
                                "id": 4,
                                "quantity": 1,
                                "kcal": 444,
                            },
                        ],
                    },
                },
            ],
        }

        url = reverse("order-detail", kwargs={"pk": self.order.pk})

        res = self.client.put(url, data=order_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["status"], -1)
        self.assertEqual(res.data["total_price"], 17000)

        order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(order.get_status_display(), "Cancelled")

    def test_order_delete(self):
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(pk=self.order.pk)
