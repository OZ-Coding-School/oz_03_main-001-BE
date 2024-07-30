from django.urls import path
from .views import SignupView, UserUpdateView, AllegiesView, UserInfoView, LoginView, LogoutView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("", UserInfoView.as_view(), name="user_info"),
    path("<int:pk>/", UserUpdateView.as_view(), name="user"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("allergies/", AllegiesView.as_view(), name="allergies"),
]
