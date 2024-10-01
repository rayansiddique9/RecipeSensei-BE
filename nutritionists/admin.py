"""This module contains the admin interface for nutritionists.
"""
from django.contrib import admin
from nutritionists.models import Nutritionist


class NutritionistAdmin(admin.ModelAdmin):
    list_display = ("user", "is_verified", "qualification", "years_of_experience")

admin.site.register(Nutritionist, NutritionistAdmin)

