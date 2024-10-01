"""This module contains the admin interface for user profiles.
"""
from django.contrib import admin
from authentication.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_verified")
    filter_horizontal = ("saved_recipes",)

admin.site.register(UserProfile, UserProfileAdmin)

