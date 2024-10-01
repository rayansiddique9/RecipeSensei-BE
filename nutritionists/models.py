"""This module contains the nutritionist related models.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authentication.models import CustomUserManager


class NutritionistManager(models.Manager):
    """For creating nutritionist profile.
    """
    def create_nutritionist(self, user_data, qualification, years_of_experience):
        user = CustomUserManager().create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )
        return self.create(user=user, qualification=qualification, years_of_experience=years_of_experience)


class Nutritionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="nutritionist")
    qualification = models.TextField(blank=True)
    years_of_experience = models.IntegerField()
    is_verified = models.BooleanField(default=False)

    objects = NutritionistManager()

    def __str__(self):
        return self.user.username

