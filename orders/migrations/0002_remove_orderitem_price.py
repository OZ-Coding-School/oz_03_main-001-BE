# Generated by Django 5.0.7 on 2024-07-24 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="price",
        ),
    ]