from django.contrib import admin

from .models import Allergy


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):  # type: ignore
    pass
