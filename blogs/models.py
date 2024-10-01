"""This module contains the blog related models.
"""
from django.db import models
from blogs.choices import STATUS_CHOICES
from blogs.constants import PENDING
from nutritionists.models import Nutritionist


class Blog(models.Model):
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=300)
    content = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

