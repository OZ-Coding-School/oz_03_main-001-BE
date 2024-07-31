from django.db import migrations, models


def create_allergies(apps, schema_editor):
    Allergy = apps.get_model("common", "Allergy")
    allergies = [
        "메밀",
        "밀",
        "대두",
        "호두",
        "땅콩",
        "복숭아",
        "토마토",
        "난류(가금류)",
        "우유",
        "닭고기",
        "소고기",
        "돼지고기",
        "새우",
        "고등어",
        "홍합",
        "전복",
        "굴",
        "조개류",
        "게",
        "오징어",
        "아황산류",
    ]

    for allergy in allergies:
        Allergy.objects.create(name=allergy)


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="allergy",
            name="name",
            field=models.CharField(
                choices=[
                    ("메밀", "Buckwheat"),
                    ("밀", "Wheat"),
                    ("대두", "Soybean"),
                    ("호두", "Walnut"),
                    ("땅콩", "Peanut"),
                    ("복숭아", "Peach"),
                    ("토마토", "Tomato"),
                    ("난류(가금류)", "Egg"),
                    ("우유", "Milk"),
                    ("닭고기", "Chicken"),
                    ("소고기", "Beef"),
                    ("돼지고기", "Pork"),
                    ("새우", "Shrimp"),
                    ("고등어", "Mackerel"),
                    ("홍합", "Mussel"),
                    ("전복", "Abalone"),
                    ("굴", "Oyster"),
                    ("조개류", "Shellfish"),
                    ("게", "Crab"),
                    ("오징어", "Squid"),
                    ("아황산류", "Sulfite"),
                ],
                max_length=20,
                unique=True,
                verbose_name="알레르기 유형",
            ),
        ),
        migrations.RunPython(create_allergies),
    ]
