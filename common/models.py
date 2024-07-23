from django.db import models


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Allergy(models.Model):
    class AllergyType(models.TextChoices):
        BUCKWHEAT = "메밀"
        WHEAT = "밀"
        SOYBEAN = "대두"
        WALNUT = "호두"
        PEANUT = "땅콩"
        PEACH = "복숭아"
        TOMATO = "토마토"
        EGG = "난류(가금류)"
        MILK = "우유"
        CHICKEN = "닭고기"
        BEEF = "소고기"
        PORK = "돼지고기"
        SHRIMP = "새우"
        MACKEREL = "고등어"
        MUSSEL = "홍합"
        ABALONE = "전복"
        OYSTER = "굴"
        SHELLFISH = "조개류"
        CRAB = "게"
        SQUID = "오징어"
        SULFITE = "아황산류"

    name = models.CharField(max_length=20, choices=AllergyType.choices, unique=True, verbose_name="알레르기 유형")

    def __str__(self) -> str:
        return self.get_name_display()

    class Meta:
        verbose_name = "알레르기"
        verbose_name_plural = "알레르기 목록"
