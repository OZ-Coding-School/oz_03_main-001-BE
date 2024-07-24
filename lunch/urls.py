from django.urls import path

from .views import LunchDetail, LunchList

urlpatterns = [
    path("", LunchList.as_view(), name="lunch-list"),
    path("<int:pk>/", LunchDetail.as_view(), name="lunch-detail"),
]
