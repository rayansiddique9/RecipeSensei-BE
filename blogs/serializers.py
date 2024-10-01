"""This module contains the serializers for blogs.
"""
from rest_framework import serializers
from blogs.models import Blog
from blogs.constants import PENDING


class BlogSerializer(serializers.ModelSerializer):
    """Blog serializer.
    """
    nutritionist = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ["id", "nutritionist", "title", "content", "status", "created_at", "modified_at"]

    def get_nutritionist(self, obj):
        from nutritionists.serializers import NutritionistSerializer
        return NutritionistSerializer(obj.nutritionist).data
    
    def get_status(self, obj):
        return obj.get_status_display()
    

class BlogUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a blog"s title and content. Status is automatically set to Pending on update.
    """

    class Meta:
        model = Blog
        fields = ["title", "content"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.status = PENDING
        instance.save()
        return instance
    
