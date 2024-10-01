"""This module contains the api endpoints for nutritionist related views.
"""
from django.urls import path
from nutritionists.views import (
    NutritionistListAPIView,
    NutritionistDetailAPIView,
    NutritionistCreateAPIView,
    NutritionistUpdateAPIView,
)


urlpatterns = [
    path("", NutritionistListAPIView.as_view(), name="nutritionist-list"),
    path("create/", NutritionistCreateAPIView.as_view(), name="nutritionist-create"),
    path("detail/", NutritionistDetailAPIView.as_view(), name="nutritionist-detail"),
    path("update/", NutritionistUpdateAPIView.as_view(), name="nutritionist-update"),
]

