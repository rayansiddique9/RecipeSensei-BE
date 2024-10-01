"""This module contains the api endpoints for user profile related views.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import (
    EmailVerificationAPIView,
    UserCreateAPIView,
    UserDetailAPIView,
    UserDeleteAPIView,
    UserListAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserUpdateAPIView,
)


urlpatterns = [
    path("", UserListAPIView.as_view(), name="user-list"),
    path("create/", UserCreateAPIView.as_view(), name="user-create"),
    path("detail/", UserDetailAPIView.as_view(), name="user-detail"),
    path("update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("logout/", UserLogoutAPIView.as_view(), name="user-logout"),
    path("delete/<str:username>", UserDeleteAPIView.as_view(), name="user-delete"),
    path("verify-email/<str:token1>/<str:token2>", EmailVerificationAPIView.as_view(), name="user-verify-email"),
    path("token-refresh/", TokenRefreshView.as_view(), name="user-token-refresh"),
]

