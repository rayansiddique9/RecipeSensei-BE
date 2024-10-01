"""This module contains the recipe related models.
"""
from django.db import models


class Recipe(models.Model):
    creator = models.ForeignKey("authentication.UserProfile", on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to="recipes/", default="recipes/default.jpg")
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
