from django.db import models

from common.models import CommonModel, Allergy


class Menu(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    kcal = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    price = models.PositiveIntegerField(default=0)

    class Category(models.TextChoices):
        BOB = "bob", "밥"
        GUK = "guk", "국"
        CHAN = "chan", "반찬"
        SIDE = "side", "사이드"

    category = models.CharField(
        max_length=4,
        choices=Category.choices,
        default=Category.CHAN,
    )


class MenuDetailCategory(CommonModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_details')
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE, related_name='allergy_details', null=True, blank=True)
    detail_category = models.CharField(max_length=30)
