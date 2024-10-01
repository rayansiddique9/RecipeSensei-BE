"""This module contains the serializers for user related models.
"""
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from recipes.serializers import RecipeSerializer
from authentication.models import UserProfile


class UserUpdateSerializer(serializers.ModelSerializer):
    """User serializer.
    """
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def update(self, instance, validated_data):
        username = validated_data.get("username", instance.username)
        email = validated_data.get("email", instance.email)
        password = validated_data.get("password")
        instance.username = username
        instance.email = email

        if password:
            instance.set_password(password)

        instance.save()
        return instance
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """The custom serializer for login with custom validate method that checks if a user has a profile and is veri-
    fied for user authentication.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        if self.user and not self.user.is_staff and not self.user.is_superuser:
            profile = None
            is_nutrtionist = False

            if hasattr(self.user, "profile"):
                profile = self.user.profile
            elif hasattr(self.user, "nutritionist"):
                profile = self.user.nutritionist
                is_nutrtionist = True

            if not profile:
                raise serializers.ValidationError("Profile for given user does not exist.")
                
            if not profile.is_verified:
                raise serializers.ValidationError("User is not verified.")
             
            data.update({
                "user": {
                    "username": self.user.username,
                    "email": self.user.email,
                    "is_nutritionist": is_nutrtionist,
                }
            })
        return data


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """User profile serializer with custom create method.
    """
    user = UserUpdateSerializer()
    saved_recipes = RecipeSerializer(many=True, required=False)
    
    class Meta:
        model = UserProfile
        fields = ["user", "saved_recipes", "is_nutritionist", "is_verified"]
        extra_kwargs = {
            "is_nutritionist": {"read_only": True},
            "is_verified": {"read_only": True},
            "saved_recipes": {"read_only": True},
            "posted_recipes": {"read_only": True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        try:
            profile = UserProfile.objects.create_profile(user_data=user_data)
        except ValidationError as error:
            raise serializers.ValidationError({"detail": error.message})
        return profile
    

class CustomUserProfileSerializer(serializers.ModelSerializer):
    """Custom user profile that only returns the user and his verification status.
    """
    user = UserUpdateSerializer()

    class Meta:
        model = UserProfile
        fields = ["user", "is_verified"]

