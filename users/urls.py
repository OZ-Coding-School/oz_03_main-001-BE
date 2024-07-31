from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views
from .views import AllegiesView, LoginView, LogoutView, SignupView, UserUpdateView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("", UserUpdateView.as_view(), name="user"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("allergies/", AllegiesView.as_view(), name="allergies"),
    # simple JWT
    path("login/simpleJWT", TokenObtainPairView.as_view()),
    path("login/simpleJWT/refresh", TokenRefreshView.as_view()),
    path("login/simpleJWT/verify", TokenVerifyView.as_view()),
    path("login/jwt/info", views.UserDetailView.as_view()),
]
