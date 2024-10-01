"""This module generates the verification url (using the registered user primary key and the unique token) for the email
verification api.
"""
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.token import account_activation_token
from authentication.constants import EMAIL_VERIFICATION_URL


def generate_verification_url(user):
    token1 = urlsafe_base64_encode(force_bytes(user.pk))
    token2 = account_activation_token.make_token(user)
    frontend_url = f"{EMAIL_VERIFICATION_URL}/{token1}/{token2}"
    return frontend_url


def generate_user_tokens(user):
    refresh = RefreshToken.for_user(user)
    return(
        {
            "refresh token": str(refresh),
            "access token": str(refresh.access_token),
        }
    )

