"""This module contains the admin interface for recipes.
"""
from django.contrib import admin
from recipes.models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "image", "is_public")

admin.site.register(Recipe, RecipeAdmin)

