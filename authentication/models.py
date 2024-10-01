"""This module contains the user related models.
"""
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserManager(BaseUserManager):
    """Manager for handling common user creation logic.
    """
    def create_user(self, username, email, password):
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


class UserProfileManager(models.Manager):
    """For user profile creation using Custom User Manager.
    """
    def create_profile(self, user_data):
        user = CustomUserManager().create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )
        return self.create(user=user)
        


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    saved_recipes = models.ManyToManyField("recipes.Recipe", related_name="saved_by_users", blank=True)
    is_nutritionist = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username
    
