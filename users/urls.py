from django.urls import path
from .views import LoginView, LogoutView, UserInfoView, CreateUserView

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("info/", UserInfoView.as_view(), name="user_info"),
]
