from django.db import models


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Allergy(models.Model):
    class AllergyType(models.TextChoices):
        BUCKWHEAT = "BUCK", "메밀"
        WHEAT = "WHEA", "밀"
        SOYBEAN = "SOYB", "대두"
        WALNUT = "WALN", "호두"
        PEANUT = "PEAN", "땅콩"
        PEACH = "PEAC", "복숭아"
        TOMATO = "TOMA", "토마토"
        EGG = "EGG", "난류(가금류)"
        MILK = "MILK", "우유"
        CHICKEN = "CHIC", "닭고기"
        BEEF = "BEEF", "소고기"
        PORK = "PORK", "돼지고기"
        SHRIMP = "SHRI", "새우"
        MACKEREL = "MACK", "고등어"
        MUSSEL = "MUSS", "홍합"
        ABALONE = "ABAL", "전복"
        OYSTER = "OYST", "굴"
        SHELLFISH = "SHEL", "조개류"
        CRAB = "CRAB", "게"
        SQUID = "SQUI", "오징어"
        SULFITE = "SULF", "아황산류"

    name = models.CharField(max_length=4, choices=AllergyType.choices, unique=True, verbose_name="알레르기 유형")

    def __str__(self) -> str:
        return self.get_name_display()

    class Meta:
        verbose_name = "알레르기"
        verbose_name_plural = "알레르기 목록"
