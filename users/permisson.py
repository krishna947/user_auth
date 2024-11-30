from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserToken


class IsTokenActive(BasePermission):
    """
    Custom permission to check if the JWT token is active (not blacklisted).
    """

    def has_permission(self, request, view):
        # Extract the access token from the Authorization header (Bearer token)
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthenticationFailed("Authorization header is missing")

        try:
            token = auth_header.split()[1]
            user_token = UserToken.objects.filter(access_token=token, is_active=True)
            if user_token.exists():
                return True
        except Exception as e:
            raise AuthenticationFailed(f"An error occurred: {str(e)}")
