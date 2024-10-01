"""This module contains the api endpoints for recipe related views.
"""
from django.urls import path
from recipes.views import (
    GenerateRecipeAPIView,
    PrivateRecipeListAPIView,
    PostedRecipeListAPIView,
    PublicRecipeListAPIView,
    RecipeCreateAPIView,
    RecipeUpdateAPIView,
    RecipeDeleteAPIView,
    SaveRecipeAPIView,
    NonPostedPublicRecipeListAPIView,
)


urlpatterns = [
    path("create/", RecipeCreateAPIView.as_view(), name="recipe-create"),
    path("public/", PublicRecipeListAPIView.as_view(), name="recipe-public-list"),
    path("private/", PrivateRecipeListAPIView.as_view(), name="recipe-private-list"),
    path("save/<int:id>", SaveRecipeAPIView.as_view(), name="recipe-save"),
    path("posted/", PostedRecipeListAPIView.as_view(), name="recipe-posted-list"),
    path("update/<int:pk>", RecipeUpdateAPIView.as_view(), name="recipe-update"),
    path("delete/<int:pk>", RecipeDeleteAPIView.as_view(), name="recipe-delete"),
    path("generate/", GenerateRecipeAPIView.as_view(), name="recipe-generate"),
    path("public-non-posted/", NonPostedPublicRecipeListAPIView.as_view(), name="recipe-public-list-others"),
]

