from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lunch.models import Lunch
from menus.models import Menu
from utils.test_helper import create_menu


class LunchAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="test@naver.com", password="1234")

        lunch = Lunch.objects.create(
            store=user,
            name="test Lunch",
            description="test lunch set",
            image_url="http://example.com/image.jpg",
        )

        menu1 = create_menu(name="test_menu1")
        menu2 = create_menu(name="test_menu2")

        lunch.menus.add(menu1, menu2)
        lunch.total_price = menu1.price + menu2.price
        lunch.save()

    def test_lunch_get(self):
        lunch = Lunch.objects.get(id=1)
        print(Lunch, lunch.name, lunch.total_price, lunch.store)

        menus = lunch.menus.all()

        print(menus)

        for menu in menus:
            print(menu.name)

    def test_lunch_post(self):
        pass

    def test_lunch_put(self):
        pass

    def test_lunch_delete(self):
        pass
