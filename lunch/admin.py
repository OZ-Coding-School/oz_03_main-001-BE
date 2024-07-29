from django.contrib import admin

from lunch.models import Lunch, LunchMenu


@admin.register(Lunch)
class LunchAdmin(admin.ModelAdmin):  # type: ignore
    pass


@admin.register(LunchMenu)
class LunchMenuAdmin(admin.ModelAdmin):  # type: ignore
    pass
