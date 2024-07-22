from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    kcal = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    price = models.PositiveIntegerField(default=0)
    category = models.enum