"""This module contains the serializers for recipes.
"""
from rest_framework import serializers
from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe serializer with custom get_Creator method that returns creator user name.
    """
    creator = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            "id",
            "creator",
            "title",
            "ingredients",
            "instructions",
            "is_public",
            "image",
            "created_at",
            "modified_at"
        ]
        
    def get_creator(self, obj):
        return obj.creator.user.username
    

class IngredientsSerializer(serializers.Serializer):
    """Ingredients serializer for the generate recipe view.
    """
    ingredients = serializers.CharField(required=True, allow_blank=False)

