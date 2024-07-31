from django.urls import path

from .views import LunchDetail, LunchList, LunchRandomList

urlpatterns = [
    path("", LunchList.as_view(), name="lunch-list"),
    path("<int:pk>/", LunchDetail.as_view(), name="lunch-detail"),
    path("random/", LunchRandomList.as_view(), name="lunch-random"),
]
