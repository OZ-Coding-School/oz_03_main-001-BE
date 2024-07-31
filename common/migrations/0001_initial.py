# Generated by Django 5.0.7 on 2024-07-23 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Allergy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("BUCK", "메밀"),
                            ("WHEA", "밀"),
                            ("SOYB", "대두"),
                            ("WALN", "호두"),
                            ("PEAN", "땅콩"),
                            ("PEAC", "복숭아"),
                            ("TOMA", "토마토"),
                            ("EGG", "난류(가금류)"),
                            ("MILK", "우유"),
                            ("CHIC", "닭고기"),
                            ("BEEF", "소고기"),
                            ("PORK", "돼지고기"),
                            ("SHRI", "새우"),
                            ("MACK", "고등어"),
                            ("MUSS", "홍합"),
                            ("ABAL", "전복"),
                            ("OYST", "굴"),
                            ("SHEL", "조개류"),
                            ("CRAB", "게"),
                            ("SQUI", "오징어"),
                            ("SULF", "아황산류"),
                        ],
                        max_length=20,
                        unique=True,
                        verbose_name="알레르기 유형",
                    ),
                ),
            ],
            options={
                "verbose_name": "알레르기",
                "verbose_name_plural": "알레르기 목록",
            },
        ),
    ]