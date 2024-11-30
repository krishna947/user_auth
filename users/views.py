from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, UserToken
from rest_framework import status
from .permisson import IsTokenActive


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            print(refresh)
            r_t = str(refresh)
            a_t = str(refresh.access_token)
            UserToken.objects.create(user=user, access_token=a_t, refresh_token=r_t)
            return Response(
                {
                    "refresh": r_t,
                    "access": a_t,
                }
            )
        return Response({"error": "Invalid credentials"}, status=401)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated, IsTokenActive]

    def get(self, request):
        try:
            user = request.user
            return Response(
                {
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "phone": user.phone,
                }
            )
        except Exception as e:
            return Response({"error": "Invalid user"}, status=401)


class CreateUserView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        phone = data.get("phone")

        if not email or not password or not firstname or not lastname:
            return Response(
                {"error": "Email, password, firstname, and lastname are required."}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email, password=password, firstname=firstname, lastname=lastname, phone=phone
        )
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, IsTokenActive]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            access_token = request.headers.get("Authorization").split()[1]

            if not refresh_token or not access_token:
                return Response({"error": "Tokens are required."}, status=status.HTTP_400_BAD_REQUEST)

            UserToken.objects.filter(access_token=access_token, refresh_token=refresh_token).update(is_active=False)
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
