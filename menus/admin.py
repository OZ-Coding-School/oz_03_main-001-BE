from django.contrib import admin

from .models import Menu, MenuDetailCategory


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):  # type: ignore
    pass


@admin.register(MenuDetailCategory)
class MenuDetailCategoryAdmin(admin.ModelAdmin):  # type: ignore
    pass
