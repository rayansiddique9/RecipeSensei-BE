"""This module contains the api endpoints for blogs related views.
"""
from django.urls import path
from blogs.views import (
    ApprovedBlogListAPIView,
    BlogCreateAPIView,
    BlogDeleteAPIView,
    BlogStatusUpdateAPIView,
    BlogUpdateAPIView,
    NutritionistApprovedBlogListAPIView,
    PendingBlogListAPIView,
    RejectedBlogListAPIView,
)


urlpatterns = [
    path("create/", BlogCreateAPIView.as_view(), name="blog-create"),
    path("delete/<int:pk>", BlogDeleteAPIView.as_view(), name="blog-delete"),
    path("update/<int:pk>", BlogUpdateAPIView.as_view(), name="blog-update"),
    path("approved/", ApprovedBlogListAPIView.as_view(), name="blog-approved-list"),
    path("posted-approved/", NutritionistApprovedBlogListAPIView.as_view(), name="blog-posted-approved-list"),
    path("rejected/", RejectedBlogListAPIView.as_view(), name="blog-rejected-list"),
    path("pending/", PendingBlogListAPIView.as_view(), name="blog-pending-list"),
    path("update-status/<int:pk>", BlogStatusUpdateAPIView.as_view(), name="blog-status-update"),
]

