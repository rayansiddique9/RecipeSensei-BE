"""This module contains the admin interface for blogs.
"""
from django.contrib import admin
from blogs.models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "nutritionist", "status", "created_at")

admin.site.register(Blog, BlogAdmin)

