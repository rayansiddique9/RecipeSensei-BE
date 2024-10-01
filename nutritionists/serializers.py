"""This module contains the serializers for nutritionists.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from nutritionists.models import Nutritionist
from authentication.serializers import UserUpdateSerializer


class NutritionistCreateSerializer(serializers.ModelSerializer):
    """Nutritionist serializer with custom create method.
    """
    user = UserUpdateSerializer()
    
    class Meta:
        model = Nutritionist
        fields = ["user", "qualification", "years_of_experience"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        qualification = validated_data.get("qualification")
        years_of_experience = validated_data.get("years_of_experience")

        try:
            profile = Nutritionist.objects.create_nutritionist(
                user_data=user_data, 
                qualification=qualification, 
                years_of_experience=years_of_experience
            )
        except ValidationError as error:
            raise serializers.ValidationError({"detail": error.message})
        return profile
    

class NutritionistSerializer(serializers.ModelSerializer):
    """Custom nutritionist profile serializer that returns specific fields.
    """
    user = UserUpdateSerializer()

    class Meta:
        model = Nutritionist
        fields = ["user", "qualification", "years_of_experience", "is_verified"]
    
