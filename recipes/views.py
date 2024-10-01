"""This module contains the recipe related views.
"""
from rest_framework import status, filters
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from recipes.models import Recipe
from recipes.serializers import IngredientsSerializer, RecipeSerializer
from recipes.constants import RECIPE_GENERATION_PROMPT
from recipes.utils import getGeminiModel


User = get_user_model()

class PublicRecipeListAPIView(ListAPIView):
    """Returns the public recipes.
    """
    serializer_class = RecipeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "ingredients", "instructions"]

    def get_queryset(self):
        return Recipe.objects.filter(is_public=True)
    

class NonPostedPublicRecipeListAPIView(ListAPIView):
    """Returns the public recipes excluding the public recipes posted by current authenticated user.
    """
    serializer_class = RecipeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "ingredients", "instructions"]

    def get_queryset(self):
        user = self.request.user.profile
        return Recipe.objects.filter(is_public=True).exclude(creator=user)


class PrivateRecipeListAPIView(ListAPIView):
    """Returns the private recipes.
    """
    serializer_class = RecipeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(is_public=False)


class SaveRecipeAPIView(APIView):
    """Saves/unsaves a recipe for the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user.profile

        if recipe not in user.saved_recipes.all():
            user.saved_recipes.add(recipe)
            return Response({"message": "Recipe saved successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Recipe already saved."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user.profile

        if recipe in user.saved_recipes.all():
            user.saved_recipes.remove(recipe)
            return Response({"message": "Recipe removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Recipe not found in saved recipes."}, status=status.HTTP_400_BAD_REQUEST)
        

class PostedRecipeListAPIView(ListAPIView):
    """Get the recipes posted by the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    
    def get_queryset(self):
        return Recipe.objects.filter(creator=self.request.user.profile).select_related("creator")
    

class RecipeCreateAPIView(CreateAPIView):
    """Adds a recipe created by the current authenticated user to the database. 
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.profile)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Recipe added successfully"}, status=status.HTTP_201_CREATED)


class RecipeUpdateAPIView(UpdateAPIView):
    """Updates a recipe. Also, removes the recipe from saved recipes of all the users if marked private during update.
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer, partial=True):
        recipe = self.get_object()
        was_public = recipe.is_public
        serializer.save()
        updated_recipe = self.get_object()
          
        if not updated_recipe.is_public and was_public:
            Recipe.saved_by_users.through.objects.filter(recipe_id=recipe.id).delete()

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({"message": "Recipe updated successfully"}, status=status.HTTP_200_OK)


class RecipeDeleteAPIView(DestroyAPIView):
    """Deletes a recipe for an authenticated user.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

class GenerateRecipeAPIView(APIView):
    """Generates a recipe for given ingredients provided by logged in user using AI model.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = IngredientsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ingredients = serializer.validated_data["ingredients"]

        model = getGeminiModel()
        response = model.generate_content(f"{RECIPE_GENERATION_PROMPT} {ingredients}")
        content = response.text
        return Response({"recipe": content}, status=status.HTTP_200_OK)
    
