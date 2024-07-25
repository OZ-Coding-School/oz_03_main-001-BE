from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders.serializers import OrderSerializer
from utils.test_helper import create_menu


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
                        "menus": [
                            {
                                "id": 1,
                                "quantity": 1,
                                "kcal": 400,
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
                                "kcal": 400,
                            },
                            {
                                "id": 4,
                                "quantity": 1,
                                "kcal": 500,
                            },
                        ],
                    },
                },
            ],
        }
        for i in range(15):
            serializer = OrderSerializer(data=self.order_data)
            serializer.is_valid()
            self.order = serializer.save()

    def test_order_list_get(self):
        url = reverse("order-list")

        with self.assertNumQueries(4):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

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
        self.assertEqual(res.data['items'][1]['lunch']['id'], 30)

