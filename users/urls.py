from django.urls import path
from .views import SignupView, UserUpdateView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("<int:pk>/", UserUpdateView.as_view(), name="user"),
]
