"""This module contains the blog related views.
"""
from rest_framework import status, filters
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from blogs.constants import APPROVED, PENDING, REJECTED
from blogs.models import Blog
from blogs.serializers import BlogSerializer, BlogUpdateSerializer


User = get_user_model()

class ApprovedBlogListAPIView(ListAPIView):
    """Lists all approved blogs.
    """
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def get_queryset(self):
        return Blog.objects.filter(status=APPROVED)
    

class NutritionistApprovedBlogListAPIView(ListAPIView):
    """Lists all approved blogs of authenticated nutritionist.
    """
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Blog.objects.filter(status=APPROVED)
        return Blog.objects.filter(status=APPROVED, nutritionist=user.nutritionist)
    

class RejectedBlogListAPIView(ListAPIView):
    """Lists all rejected blogs of authenticated nutritionist.
    """
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Blog.objects.filter(status=REJECTED)
        return Blog.objects.filter(status=REJECTED, nutritionist=user.nutritionist)
    

class PendingBlogListAPIView(ListAPIView):
    """Lists all pending blogs authenticated nutritionist.
    """
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Blog.objects.filter(status=PENDING)
        return Blog.objects.filter(status=PENDING, nutritionist=user.nutritionist)
      

class BlogCreateAPIView(CreateAPIView):
    """Adds a blog created by the current authenticated user to the database. 
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        serializer.save(nutritionist=self.request.user.nutritionist)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Blog added successfully and sent for review"}, status=status.HTTP_201_CREATED)


class BlogDeleteAPIView(DestroyAPIView):
    """Deletes a blog
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class BlogUpdateAPIView(UpdateAPIView):
    """Updates a blog.
    """
    serializer_class = BlogUpdateSerializer
    queryset = Blog.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Blog updated successfully and sent for review"}, status=status.HTTP_200_OK)
    

class BlogStatusUpdateAPIView(UpdateAPIView):
    """Approves a blog posted by nutritionist.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.status = request.data.get("status")
        blog.save()
        return Response({"message": "Blog status updated successfully"}, status=status.HTTP_200_OK)

