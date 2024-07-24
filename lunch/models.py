from django.contrib.auth.models import User
from django.db import models

from common.models import CommonModel


class Lunch(CommonModel):
    # TODO: store 모델 생성하면 변경 필요
    store = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="도시락")
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    total_price = models.PositiveIntegerField(default=0)
    menus = models.ManyToManyField("menus.Menu", through="lunch.LunchMenu", blank=True)
    total_kcal = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class LunchMenu(CommonModel):
    menu = models.ForeignKey("menus.Menu", on_delete=models.CASCADE)
    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    kcal = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["menu", "lunch"], name="unique_lunch_menu"),
        ]

    def __str__(self) -> str:
        return f"{self.menu.name} - {self.lunch.name}"
