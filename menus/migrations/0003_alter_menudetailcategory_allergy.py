# Generated by Django 5.0.7 on 2024-07-23 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
        ("menus", "0002_alter_menu_category_menudetailcategory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menudetailcategory",
            name="allergy",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="common.allergy"
            ),
        ),
    ]
