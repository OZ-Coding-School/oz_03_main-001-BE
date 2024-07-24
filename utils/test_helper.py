from menus.models import Menu
from menus.serializers import MenuWithDetailSerializer


def create_menu(name: str) -> Menu:

    menu_data = {
        "name": name,
        "description": "descriptionnnsss",
        "kcal": 333,
        "image_url": "https://naver.com",
        "price": 1000,
        "category": "bob",
        "menu_details": [
            {"allergy": "메밀", "detail_category": "상세 카테고리1"},
            {"allergy": None, "detail_category": "상세 카테고리2"},
        ],
    }

    serializer = MenuWithDetailSerializer(data=menu_data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()
