"""This module contains the authentication APIs.
"""
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.models import UserProfile
from authentication.serializers import (
    CustomTokenObtainPairSerializer,
    CustomUserProfileSerializer,
    UserProfileCreateSerializer,
    UserUpdateSerializer,
)
from authentication.token import account_activation_token
from authentication.tasks import send_verification_email
from authentication.utils import generate_verification_url


User = get_user_model()

class UserLoginAPIView(TokenObtainPairView):
    """Custom login view that returns the nutritionist status along with jwt tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError as e:
            error_message = e.detail.get("non_field_errors", ["Error"])[0]
            return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    """Logs out the user and blaclists the refresh token used.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Error during logout. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
        

class EmailVerificationAPIView(APIView):
    """API for verifying user email and providing JWT tokens on successfull verification.
    """
    def get(self, request, token1, token2, *args, **kwargs):
        user_pk = force_str(urlsafe_base64_decode(token1))
        user = User.objects.filter(pk=user_pk).first()

        if not user:
            return Response(
                {
                    "error": "User not found. Register again.",
                },
                status = status.HTTP_404_NOT_FOUND
            )

        if not account_activation_token.check_token(user, token2):
            return Response(
                {
                    "error": "User could not be verified. Register again.",
                },
                status = status.HTTP_401_UNAUTHORIZED
            )
        profile = None
        if hasattr(user, "profile"):
            profile = user.profile
        else:
            profile = user.nutritionist

        if not profile:
            return Response(
                {
                    "error": "No profile associated with given user. Please register again",
                },
                status = status.HTTP_404_NOT_FOUND
            )

        profile.is_verified = True
        profile.save()
        return Response(
            {
                "message": "User verified successfully"
            },
            status=status.HTTP_200_OK
        )


class UserDeleteAPIView(DestroyAPIView):
    """Deletes profile of a user/nutritionist who has to be logged in. No authenticated user can delete the account of
    another user.
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        if user != request.user and not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to delete this account."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        user.delete()
        return Response({"message": "Account deleted successfully!"}, status=status.HTTP_200_OK)
    

class UserCreateAPIView(CreateAPIView):
    """Registers the user and sends verification link to the provided email.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        user = profile.user
        verification_url = generate_verification_url(user)
        
        send_verification_email.delay(
            recepient_email=serializer.data["user"]["email"],
            verification_url=verification_url,
        )
        return Response(
            {
                "message": "User registered and verification link sent to provided email.",
            },
            status=status.HTTP_201_CREATED
        )


class UserListAPIView(ListAPIView):
    """Lists all the user profiles, verified and unverified.
    """
    serializer_class = CustomUserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return UserProfile.objects.filter(is_verified=True)


class UserDetailAPIView(RetrieveAPIView):
    """Retrieves the user profile.
    """
    queryset = UserProfile.objects.prefetch_related("saved_recipes")
    serializer_class = UserProfileCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class UserUpdateAPIView(UpdateAPIView):
    """Updates a user profile.
    """
    serializer_class = UserUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data

        if "username" in data and User.objects.exclude(pk=user.pk).filter(username=data["username"]).exists():
            raise ValidationError({"message": "A user with that username already exists."})
        
        if "email" in data and User.objects.exclude(pk=user.pk).filter(email=data["email"]).exists():
            raise ValidationError({"message": "A user with that email already exists."})

        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"user": serializer.data, "message": "Profile updated successfully"}, status=status.HTTP_200_OK)
    
