from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CommonModel


class Menu(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    kcal = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    price = models.PositiveIntegerField(default=0)

    class Category(models.TextChoices):
        BOB = "bo", _("bob")
        GUK = "gu", _("guk")
        CHAN = "ch", _("chan")
        SIDE = "si", _("side")

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.CHAN,
    )
