"""This module contains the views for nutritionist profile.
"""
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from nutritionists.models import  Nutritionist
from nutritionists.serializers import NutritionistCreateSerializer, NutritionistSerializer
from authentication.serializers import UserUpdateSerializer
from authentication.tasks import send_verification_email
from authentication.utils import generate_verification_url


User = get_user_model()

class NutritionistCreateAPIView(CreateAPIView):
    """Registers the nutritionist and sends verification link to the provided email.
    """
    queryset = Nutritionist.objects.all()
    serializer_class = NutritionistCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nutritionist = serializer.save()
        user = nutritionist.user
        verification_url = generate_verification_url(user)
        
        send_verification_email.delay(
            recepient_email=serializer.data["user"]["email"],
            verification_url=verification_url,
        )
        return Response(
            {
                "message": "Nutritionist registered and verification link sent to provided email.",
            },
            status=status.HTTP_201_CREATED
        )


class NutritionistListAPIView(ListAPIView):
    serializer_class = NutritionistSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Nutritionist.objects.filter(is_verified=True)
    

class NutritionistDetailAPIView(RetrieveAPIView):
    """Retrives the nutritionist profile.
    """
    queryset = Nutritionist.objects.all()
    serializer_class = NutritionistCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Nutritionist.objects.get(user=self.request.user) 
    

class NutritionistUpdateAPIView(UpdateAPIView):
    """Updates the nutritionist profile.
    """
    serializer_class = NutritionistCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.nutritionist
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        user_data = request.data.get("user", {})
        email = user_data.get("email")
        username = user_data.get("username")

        if username and User.objects.exclude(pk=profile.user.pk).filter(username=username).exists():
            return Response(
                {"message": "A user with that username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if email and User.objects.exclude(pk=profile.user.pk).filter(email=email).exists():
            return Response(
                {"message": "A user with that email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_serializer = UserUpdateSerializer(profile.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        profile.qualification = request.data.get("qualification", profile.qualification)
        profile.years_of_experience = request.data.get("years_of_experience", profile.years_of_experience) 
        profile.save()
        serializer = NutritionistCreateSerializer(profile)
        return Response({"nutritionist": serializer.data, "message": "Profile updated successfully"}, status=status.HTTP_200_OK)
    
    
